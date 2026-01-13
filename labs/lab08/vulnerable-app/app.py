from flask import (
    Flask,
    request,
    make_response,
    render_template_string,
    session,
    abort,
    send_from_directory,
)
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

DB_PATH = os.environ.get("APP_DB_PATH", "app.db")

# Важно: для лабы можно оставить дефолт, но лучше задать через env APP_SECRET_KEY
app.secret_key = os.environ.get("APP_SECRET_KEY", "lab08-dev-secret-key")

# Cookie hardening (ZAP: HttpOnly/SameSite)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    # Secure=True только при HTTPS. У тебя HTTP, поэтому False.
    SESSION_COOKIE_SECURE=False,
)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password_hash TEXT,
            role TEXT
        )
        """
    )
    cur.execute("DELETE FROM users")

    # Храним хэши паролей вместо plaintext
    cur.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        ("admin", generate_password_hash("admin123"), "admin"),
    )
    cur.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        ("user", generate_password_hash("user123"), "user"),
    )
    conn.commit()
    conn.close()


def require_admin():
    if session.get("role") != "admin":
        abort(403)


def no_store(resp):
    # ZAP informational про кеширование: на чувствительных страницах лучше no-store
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    return resp


@app.after_request
def add_security_headers(resp):
    # ZAP: CSP missing
    resp.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "form-action 'self'",
    )

    # ZAP: clickjacking header missing
    resp.headers.setdefault("X-Frame-Options", "DENY")

    # ZAP: X-Content-Type-Options missing
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")

    # ZAP: Permissions-Policy missing
    resp.headers.setdefault(
        "Permissions-Policy",
        "geolocation=(), microphone=(), camera=(), payment=(), usb=()",
    )

    # ZAP: Spectre/site isolation hardening
    resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    resp.headers.setdefault("Cross-Origin-Embedder-Policy", "require-corp")
    resp.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")

    # Уменьшаем утечки через Referrer (не требовал ZAP, но норм для hardening)
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    return resp


@app.route("/")
def index():
    username = session.get("user")
    role = session.get("role")

    html = """
    <h1>DAST Demo App (Fixed)</h1>
    <p>Это версия после исправлений по отчёту ZAP.</p>

    {% if username %}
      <p>Вы вошли как: <b>{{ username }}</b> (роль: <b>{{ role }}</b>)</p>
      <p><a href="/logout">Logout</a></p>
    {% else %}
      <p>Вы не авторизованы. <a href="/login">Login</a></p>
    {% endif %}

    <ul>
      <li><a href="/echo?msg=Hello">Echo (XSS fixed)</a></li>
      <li><a href="/search?username=admin">Search (SQLi fixed)</a></li>
      <li><a href="/profile">Profile (server-side session)</a></li>
      <li><a href="/admin">Admin (protected)</a></li>
      <li><a href="/files/secret.txt">Files (admin-only)</a></li>
    </ul>
    """
    return make_response(render_template_string(html, username=username, role=role))


@app.route("/echo")
def echo():
    # XSS fixed: экранируем пользовательский ввод
    msg = request.args.get("msg", "")
    safe_msg = escape(msg)

    template = """
    <h2>Echo (safe)</h2>
    <p>Сообщение: {{ msg }}</p>
    <p>Тут экранирование включено — JS не выполняется.</p>
    <a href="/">Назад</a>
    """
    return make_response(render_template_string(template, msg=safe_msg))


@app.route("/search")
def search():
    # SQLi fixed: параметризованный запрос, не показываем SQL в ответе (ZAP SQL disclosure)
    username = request.args.get("username", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT id, username, role FROM users WHERE username = ?",
        (username,),
    ).fetchall()
    conn.close()

    template = """
    <h2>Поиск пользователя (safe)</h2>
    <p><b>Параметр:</b> <code>{{ username }}</code></p>

    {% if rows %}
      <ul>
      {% for id, username, role in rows %}
        <li>{{ id }} — {{ username }} ({{ role }})</li>
      {% endfor %}
      </ul>
    {% else %}
      <p>Ничего не найдено</p>
    {% endif %}

    <a href="/">Назад</a>
    """
    return make_response(render_template_string(template, username=escape(username), rows=rows))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        form = """
        <h2>Логин</h2>
        <form method="post">
          <label>Username: <input type="text" name="username"></label><br>
          <label>Password: <input type="password" name="password"></label><br>
          <button type="submit">Login</button>
        </form>
        <p>admin / admin123 или user / user123</p>
        <a href="/">Назад</a>
        """
        return no_store(make_response(render_template_string(form)))

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    row = cur.execute(
        "SELECT username, password_hash, role FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()

    if row:
        uname, pwd_hash, role = row
        if check_password_hash(pwd_hash, password):
            session["user"] = uname
            session["role"] = role
            resp = make_response(f"<h2>Добро пожаловать, {escape(uname)} ({escape(role)})!</h2><a href='/'>На главную</a>")
            return no_store(resp)

    return no_store(make_response("<h2>Неверные учетные данные</h2><a href='/login'>Попробовать снова</a>"))


@app.route("/logout")
def logout():
    session.clear()
    return no_store(make_response("<h2>Вы вышли</h2><a href='/'>На главную</a>"))


@app.route("/profile")
def profile():
    username = session.get("user")
    role = session.get("role")

    if not username:
        return no_store(make_response("<h2>Вы не авторизованы</h2><a href='/login'>Login</a>", 401))

    template = """
    <h2>Профиль</h2>
    <p>Имя: {{ username }}</p>
    <p>Роль: {{ role }}</p>
    <p>Роль берётся из серверной сессии (подделка cookie больше не работает).</p>
    <a href="/">Назад</a>
    """
    return no_store(make_response(render_template_string(template, username=escape(username), role=escape(role))))


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return no_store(make_response("<h2>Доступ запрещён</h2><a href='/'>Назад</a>", 403))

    template = """
    <h2>Admin panel</h2>
    <p>Доступ только для admin через серверную сессию.</p>
    <a href="/">Назад</a>
    """
    return no_store(make_response(render_template_string(template)))


@app.route("/files/")
def files_index():
    # Directory listing fixed: не отдаём список файлов
    return "<h2>Not Found</h2>", 404


@app.route("/files/<path:filename>")
def files(filename):
    # Ограничиваем доступ к файлам: только admin
    require_admin()

    base_dir = Path(__file__).resolve().parent
    target_dir = base_dir / "files"

    # Запрещаем выдавать директории
    if filename.endswith("/") or filename == "":
        abort(404)

    # Flask сам защищает от path traversal через send_from_directory
    return no_store(send_from_directory(target_dir, filename))


if __name__ == "__main__":
    init_db()
    # debug=False уменьшает утечки и “Server” в dev может стать менее подробным
    app.run(host="0.0.0.0", port=8080, debug=False)

