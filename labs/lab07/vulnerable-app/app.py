from flask import Flask, request, make_response, abort
import sqlite3
import subprocess
import logging
import html
from pathlib import Path
import ast
import operator

app = Flask(__name__)

# === Production-safe configuration ===
app.config["DEBUG"] = False
logging.basicConfig(level=logging.INFO)

DB_PATH = "app.db"


# === Database ===
def get_db():
    return sqlite3.connect(DB_PATH)


# === Utils ===
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(node):
    """Safely evaluate arithmetic expressions without eval()."""
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Invalid constant")
        return node.value
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in OPS:
            raise ValueError("Unsupported operator")
        return OPS[op_type](
            safe_eval(node.left),
            safe_eval(node.right),
        )
    raise ValueError("Unsafe expression")


# === Routes ===
@app.route("/")
def index():
    return "Application is running"


@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    conn = get_db()
    cur = conn.cursor()

    # SQL Injection protection (parameterized query)
    cur.execute(
        "SELECT id, name, email FROM users WHERE name = ?",
        (username,),
    )
    rows = cur.fetchall()
    conn.close()
    return {"result": rows}


@app.route("/search")
def search():
    q = request.args.get("q", "")
    safe_q = html.escape(q)
    html_resp = f"<h1>Results for: {safe_q}</h1>"
    return make_response(html_resp, 200)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # No shell execution
    subprocess.run(
        ["ping", "-c", "1", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return f"Pinged {host}"


@app.route("/backup")
def backup():
    target = request.args.get("target", "backup.sql")

    # Restrict file write location
    target_path = Path("/tmp") / Path(target).name

    with open(target_path, "w") as f:
        subprocess.run(
            ["pg_dump", "mydb"],
            stdout=f,
            stderr=subprocess.DEVNULL,
            check=False,
        )

    return f"Backup written to {target_path}"


@app.route("/read")
def read_file():
    base_dir = Path("/tmp").resolve()
    requested = Path(request.args.get("path", "")).resolve()

    # Path Traversal protection
    if not str(requested).startswith(str(base_dir)):
        abort(403)

    if not requested.exists():
        abort(404)

    return requested.read_text()


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    try:
        node = ast.parse(expr, mode="eval")
        result = safe_eval(node)
        return str(result)
    except Exception:
        abort(400)


# === Entry point ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
