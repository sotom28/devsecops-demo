import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT, role TEXT)")
    conn.executemany(
        "INSERT INTO users VALUES (?, ?, ?)",
        [(1, "admin", "superuser"), (2, "profe", "docente"), (3, "ana", "estudiante")],
    )
    return conn


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/user")
def user():
    name = request.args.get("name", "")
    db = get_db()
    rows = db.execute(f"SELECT id, name, role FROM users WHERE name = '{name}'").fetchall()
    return jsonify(users=[{"id": r[0], "name": r[1], "role": r[2]} for r in rows])


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return out


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
