# frontend app
from flask import Flask, render_template, redirect, request, url_for, session
import urllib
import requests
import os

app = Flask(__name__)
app.secret_key = "final-project-secret-key"

# default to localhost for local testing
TODO_API_URL = "http://" + os.environ.get("TODO_API_IP", "127.0.0.1") + ":5001"


@app.route("/")
def home():
    # if nobody is logged in yet, send them to login
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    resp = requests.get(TODO_API_URL + "/api/items/" + username)
    tdlist = resp.json()

    return render_template("index.html", todolist=tdlist, username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        resp = requests.post(
            TODO_API_URL + "/api/register",
            json={
                "username": request.form["username"],
                "password": request.form["password"]
            }
        )

        data = resp.json()

        if data.get("result"):
            return redirect(url_for("login"))

        return render_template("register.html", message=data.get("message", "Registration failed."))

    return render_template("register.html", message="")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        resp = requests.post(
            TODO_API_URL + "/api/login",
            json={
                "username": request.form["username"],
                "password": request.form["password"]
            }
        )

        data = resp.json()

        if data.get("result"):
            # store the username in session
            session["username"] = data["username"]
            return redirect(url_for("home"))

        return render_template("login.html", message=data.get("message", "Login failed."))

    return render_template("login.html", message="")


@app.route("/logout")
def logout():
    # clear the session and go back to login
    session.clear()
    return redirect(url_for("login"))


@app.route("/add", methods=["POST"])
def add_entry():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    requests.post(
        TODO_API_URL + "/api/items/" + username,
        json={
            "what_to_do": request.form["what_to_do"],
            "due_date": request.form["due_date"]
        }
    )

    return redirect(url_for("home"))


@app.route("/delete/<item>")
def delete_entry(item):
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    item = urllib.parse.quote(item)

    requests.delete(TODO_API_URL + "/api/items/" + username + "/" + item)

    return redirect(url_for("home"))


@app.route("/mark/<item>")
def mark_as_done(item):
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    item = urllib.parse.quote(item)

    requests.put(TODO_API_URL + "/api/items/" + username + "/" + item)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
