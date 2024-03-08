from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import create_engine, text
from hashlib import sha1

tweeter = Flask(__name__)
tweeter.config["SECRET_KEY"] = "this is not secret, remember, change it!"
engine = create_engine("sqlite:///tweeter.db")


def hash_value(string):
    hash = sha1()
    hash.update(string.encode())
    return hash.hexdigest()


@tweeter.route("/")
def index():
    return render_template("index.html")


@tweeter.route("/register")
def register():
    return render_template("register.html")


@tweeter.route("/register", methods=["POST"])
def handle_register():
    pass


@tweeter.route("/users")
def users():
    pass


@tweeter.route("/users/<username>")
def user_detail(username):
    pass


@tweeter.route("/login")
def login():
    return render_template("login.html")


@tweeter.route("/login", methods=["POST"])
def handle_login():
    pass


@tweeter.route("/logout")
def logout():
    pass


@tweeter.route("/tweet", methods=["POST"])
def handle_tweet():
    pass


@tweeter.route("/follow/<followee>")
def follow(followee):
    pass


@tweeter.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@tweeter.errorhandler(403)
def unauthorized(e):
    return render_template("403.html"), 403


tweeter.run(debug=True, port=8080)
