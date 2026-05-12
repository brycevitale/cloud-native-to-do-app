# backend API
from flask import Flask, g, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import urllib
import json

DATABASE = "todolist.db"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/api/register", methods=["POST"])
def register_user():
    # make a new user account
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({
            "result": False,
            "message": "Username and password are required."
        }), 400

    db = get_db()

    existing_user = db.execute(
        "SELECT id FROM users WHERE username = ?",
        [username]
    ).fetchone()

    if existing_user:
        return jsonify({
            "result": False,
            "message": "Username already exists."
        }), 400

    password_hash = generate_password_hash(password)

    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        [username, password_hash]
    )
    db.commit()

    return jsonify({
        "result": True,
        "message": "User registered successfully."
    })


@app.route("/api/login", methods=["POST"])
def login_user():
    # check if the login info matches
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    db = get_db()

    user = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        [username]
    ).fetchone()

    if not user:
        return jsonify({
            "result": False,
            "message": "Invalid username or password."
        }), 401

    if not check_password_hash(user[2], password):
        return jsonify({
            "result": False,
            "message": "Invalid username or password."
        }), 401

    return jsonify({
        "result": True,
        "message": "Login successful.",
        "user_id": user[0],
        "username": user[1]
    })


@app.route("/api/items/<username>")
def get_items(username):
    # only pull tasks for the user that is logged in
    db = get_db()

    user = db.execute(
        "SELECT id FROM users WHERE username = ?",
        [username]
    ).fetchone()

    if not user:
        return jsonify({
            "result": False,
            "message": "User not found."
        }), 404

    cur = db.execute(
        "SELECT what_to_do, due_date, status FROM entries WHERE user_id = ?",
        [user[0]]
    )
    entries = cur.fetchall()

    tdlist = []
    for row in entries:
        tdlist.append({
            "what_to_do": row[0],
            "due_date": row[1],
            "status": row[2]
        })

    return Response(json.dumps(tdlist), mimetype="application/json")


@app.route("/api/items/<username>", methods=["POST"])
def add_item(username):
    # add a task for the current user
    data = request.json
    what_to_do = data.get("what_to_do", "").strip()
    due_date = data.get("due_date", "").strip()

    db = get_db()

    user = db.execute(
        "SELECT id FROM users WHERE username = ?",
        [username]
    ).fetchone()

    if not user:
        return jsonify({
            "result": False,
            "message": "User not found."
        }), 404

    db.execute(
        "INSERT INTO entries (user_id, what_to_do, due_date, status) VALUES (?, ?, ?, ?)",
        [user[0], what_to_do, due_date, ""]
    )
    db.commit()

    return jsonify({"result": True})


@app.route("/api/items/<username>/<item>", methods=["DELETE"])
def delete_item(username, item):
    # delete the task that matches this user
    item = urllib.parse.unquote(item)
    db = get_db()

    user = db.execute(
        "SELECT id FROM users WHERE username = ?",
        [username]
    ).fetchone()

    if not user:
        return jsonify({
            "result": False,
            "message": "User not found."
        }), 404

    db.execute(
        "DELETE FROM entries WHERE user_id = ? AND what_to_do = ?",
        [user[0], item]
    )
    db.commit()

    return jsonify({"result": True})


@app.route("/api/items/<username>/<item>", methods=["PUT"])
def update_item(username, item):
    # mark the task as done for this user
    item = urllib.parse.unquote(item)
    db = get_db()

    user = db.execute(
        "SELECT id FROM users WHERE username = ?",
        [username]
    ).fetchone()

    if not user:
        return jsonify({
            "result": False,
            "message": "User not found."
        }), 404

    db.execute(
        "UPDATE entries SET status = 'done' WHERE user_id = ? AND what_to_do = ?",
        [user[0], item]
    )
    db.commit()

    return jsonify({"result": True})


def get_db():
    # open the db if it is not already open for this request
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = sqlite3.connect(app.config["DATABASE"])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    # close it back up when the request ends
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)
