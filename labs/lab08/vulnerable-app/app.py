from flask import (
    Flask,
    request,
    make_response,
    render_template_string,
)
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.environ.get("APP_DB_PATH", "app.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
        """
    )
    cur.execute("DELETE FROM users")
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')"
    )
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES ('user', 'user123', 'user')"
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    html = """
    <h1>Vulnerable DAST Demo App</h1>
    <ul>
      <li><a href="/echo?msg=Hello">Reflected XSS / echo</a></li>
      <li><a href="/search?username=admin">SQL Injection / search</a></li>
      <li><a href="/login">Небезопасный логин</a></li>
      <li><a href="/profile">Профиль (cookie)</a></li>
      <li><a href="/admin">Admin (cookie)</a></li>
      <li><a href="/files/">Directory listing</a></li>
    </ul>
    """
    resp = make_response(html)
    resp.set_cookie("session", "guest-session-id")
    return resp


@app.route("/echo")
def echo():
    msg = request.args.get("msg", "")
    template = f"""
    <h2>Echo</h2>
    <p>Сообщение: {msg}</p>
    <p>Попробуйте: &lt;script&gt;alert('XSS')&lt;/script&gt;</p>
    <a href="/">Назад</a>
    """
    return render_template_string(template)


@app.route("/search")
def search():
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # УЯЗВИМОСТЬ СПЕЦИАЛЬНО НЕ ИСПРАВЛЯЕМ (п.10 будет фикс)
    query = f"SELECT id, username, role FROM users WHERE username = '{username}'"  # nosec B608

    rows = []
    error = None

    try:
        rows = list(cur.execute(query))
    except Exception as e:
        error = str(e)

    conn.close()

    found_count = len(rows)
    sqli_suspicion = found_count > 1  # <<< ВСЕГДА определена

    template = """
    <h2>Поиск пользователя</h2>

    <p><b>Ввод:</b> <code>{{ username }}</code></p>
    <p><b>SQL-запрос:</b> <code>{{ query }}</code></p>

    {% if error %}
      <p style="color:red;"><b>SQL error:</b> {{ error }}</p>
    {% endif %}

    {% if rows %}
      <p><b>Найдено записей:</b> {{ found_count }}</p>

      {% if sqli_suspicion %}
        <div style="background:#ffecec; padding:10px; border:1px solid red;">
          ⚠ Возможный признак <b>SQL Injection</b>: возвращено более одной записи
        </div>
      {% endif %}

      <ul>
      {% for id, username, role in rows %}
        <li>{{ id }} — {{ username }} ({{ role }})</li>
      {% endfor %}
      </ul>
    {% else %}
      <p>Ничего не найдено</p>
    {% endif %}

    <p>Payload: <code>?username=admin' OR '1'='1</code></p>
    <a href="/">Назад</a>
    """

    return render_template_string(
        template,
        username=username,
        query=query,
        rows=rows,
        error=error,
        found_count=found_count,
        sqli_suspicion=sqli_suspicion,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string("""
        <h2>Логин</h2>
        <form method="post">
          <input name="username"><br>
          <input name="password" type="password"><br>
          <button>Login</button>
        </form>
        <p>admin / admin123</p>
        <a href="/">Назад</a>
        """)

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"SELECT username, role FROM users WHERE username = '{username}' AND password = '{password}'"  # nosec
    row = cur.execute(query).fetchone()
    conn.close()

    if row:
        uname, role = row
        resp = make_response(f"<h2>Добро пожаловать, {uname} ({role})</h2><a href='/'>Назад</a>")
        resp.set_cookie("user", uname)
        resp.set_cookie("role", role)
        return resp

    return "<h2>Неверные данные</h2><a href='/login'>Назад</a>"


@app.route("/profile")
def profile():
    username = request.cookies.get("user", "guest")
    role = request.cookies.get("role", "guest")

    return render_template_string("""
    <h2>Профиль</h2>
    <p>Имя: {{ username }}</p>
    <p>Роль: {{ role }}</p>
    <p>Cookie можно подделать</p>
    <a href="/">Назад</a>
    """, username=username, role=role)


@app.route("/admin")
def admin():
    role = request.cookies.get("role", "guest")
    if role != "admin":
        return "<h2>Доступ запрещён</h2><a href='/'>Назад</a>", 403

    return """
    <h2>Admin panel</h2>
    <ul>
      <li>DEBUG = true</li>
      <li>SECRET_FLAG</li>
    </ul>
    <a href="/">Назад</a>
    """


@app.route("/files/")
@app.route("/files/<path:subpath>")
def files(subpath=""):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    target_dir = os.path.join(base_dir, "files")
    full_path = os.path.join(target_dir, subpath)

    if not os.path.exists(full_path):
        return "<h2>Путь не найден</h2><a href='/'>Назад</a>", 404

    if os.path.isdir(full_path):
        items = "".join(
            f"<li><a href='/files/{e}'>{e}</a></li>"
            for e in os.listdir(full_path)
        )
        return f"""
        <h2>Directory listing</h2>
        <ul>{items}</ul>
        <p style="color:red;">⚠ Directory listing включён</p>
        <a href="/">Назад</a>
        """

    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        return f"<pre>{f.read()}</pre>"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
