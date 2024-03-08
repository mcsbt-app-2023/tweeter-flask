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

    if "user_id" in session:
        query = text(
            """
    SELECT *
    FROM follows f
    INNER JOIN tweets t on t.user_id=f.followee_id
    INNER JOIN users u on u.id=f.followee_id
    WHERE f.follower_id=:user_id
    """
        )

        with engine.connect() as connection:
            tweets = connection.execute(query, user_id=session["user_id"])
            return render_template("index.html", tweets=tweets)

    return render_template("index.html")


@tweeter.route("/register")
def register():
    return render_template("register.html")


@tweeter.route("/register", methods=["POST"])
def handle_register():
    username = request.form["username"]
    picture = request.form["picture"]
    password = hash_value(request.form["password"])

    select_query = text(
        """
    SELECT *
    FROM users
    WHERE username=:username
    """
    )

    insert_query = text(
        """
    INSERT INTO users(username, picture, password)
    VALUES (:username, :picture, :password)
    """
    )

    with engine.connect() as connection:
        user_exists = connection.execute(select_query, username=username).fetchone()

        if user_exists:
            return "username already exists", 403

        connection.execute(
            insert_query, username=username, picture=picture, password=password
        )

        user = connection.execute(select_query, username=username).fetchone()
        session["username"] = user["username"]
        session["user_id"] = user["id"]

        return redirect("/")


@tweeter.route("/users")
def users():
    query = text(
        """
    SELECT *
    FROM USERS
    """
    )

    with engine.connect() as connection:
        users = connection.execute(query).fetchall()

        return render_template("users.html", users=users)


@tweeter.route("/users/<username>")
def user_detail(username):
    user_query = text(
        """
    SELECT *
    FROM USERS
    WHERE username=:username
    """
    )
    tweets_query = text(
        """
    SELECT *
    FROM users u
    INNER JOIN tweets t
    ON t.user_id=u.id
    WHERE u.username=:username
    """
    )

    with engine.connect() as connection:
        user = connection.execute(user_query, username=username).fetchone()
        tweets = connection.execute(tweets_query, username=username).fetchall()

        return render_template("user_detail.html", user=user, tweets=tweets)


@tweeter.route("/login")
def login():
    return render_template("login.html")


@tweeter.route("/login", methods=["POST"])
def handle_login():
    username = request.form["username"]
    password = hash_value(request.form["password"])

    query = text(
        """
        SELECT *
        FROM users
        WHERE username=:username
        AND password=:password
        """
    )

    with engine.connect() as connection:
        user = connection.execute(
            query, username=username, password=password
        ).fetchone()
        if user:
            session["username"] = user["username"]
            session["user_id"] = user["id"]
        else:
            return "user not found", 404

    return redirect("/")


@tweeter.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


@tweeter.route("/tweet", methods=["POST"])
def handle_tweet():
    tweet = request.form["tweet"]

    insert_query = text(
        """
    insert into
    tweets(tweet, user_id)
    values(:tweet, :user_id)
    """
    )

    with engine.connect() as connection:
        connection.execute(insert_query, tweet=tweet, user_id=session["user_id"])

        return redirect("/")


@tweeter.route("/follow/<followee>")
def follow(followee):

    query = text(
        """
    INSERT INTO follows(follower_id, followee_id)
    VALUES(:follower_id, :followee_id)
    """
    )

    with engine.connect() as connection:
        connection.execute(query, follower_id=session["user_id"], followee_id=followee)

        return redirect("/")


@tweeter.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@tweeter.errorhandler(403)
def unauthorized(e):
    return render_template("403.html"), 403


tweeter.run(debug=True, port=8080)
