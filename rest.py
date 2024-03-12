from flask import Flask, request, session, redirect, jsonify, abort
from sqlalchemy import create_engine, text
from hashlib import sha1

tweeter = Flask(__name__)
tweeter.config["SECRET_KEY"] = "this is not secret, remember, change it!"
engine = create_engine("sqlite:///tweeter.db")


def authenticate_request():
    username = request.authorization["username"]
    password = hash_value(request.authorization["password"])

    login_query = text(
        """
        SELECT *
        FROM users
        WHERE username=:username and password=:password
        """
    )

    with engine.connect() as connection:
        user = connection.execute(
            login_query, username=username, password=password
        ).fetchone()

        if not user:
            raise Exception("not authenticated")


def hash_value(string):
    hash = sha1()
    hash.update(string.encode())
    return hash.hexdigest()


@tweeter.route("/users", methods=["POST"])
def create_user():
    pass


@tweeter.route("/users")
def users():
    pass


@tweeter.route("/users/<username>/tweets")
def user_detail(username):
    pass


@tweeter.route("/tweets", methods=["POST"])
def handle_tweet():
    pass


tweeter.run(debug=True, port=8080)
