from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

tweeter = Flask(__name__)
tweeter.config["SECRET_KEY"] = "this is not secret, remember, change it!"
engine = create_engine("sqlite:///tweeter.db")

@tweeter.route("/")
def index():

    if "user_id" in session:
        query = f"""
        SELECT *
        FROM follows f
        INNER JOIN tweets t ON f.followee_id=t.user_id
        INNER JOIN users u ON f.followee_id=u.id
        WHERE f.follower_id={session["user_id"]}
        """


        with engine.connect() as connection:
            tweets = connection.execute(query).fetchall()

            return render_template("index.html", tweets=tweets)
    else:
        return render_template("index.html")

@tweeter.route("/register")
def register():
    return render_template("register.html")

@tweeter.route("/register", methods=["POST"])
def handle_register():
    username = request.form["username"]
    password = request.form["password"]
    picture = request.form["picture"]

    hashed_password = generate_password_hash(password)

    query = f"""
    INSERT INTO users(username, password, picture)
    VALUES ("{username}", "{hashed_password}", "{picture}")
    """

    user_query = f"""
    SELECT id
    FROM users
    WHERE username='{username}'
    """

    with engine.connect() as connection:
        connection.execute(query)
        user = connection.execute(user_query).fetchone()

        session["username"] = username
        session["user_id"] = user[0]

        return redirect(url_for("index"))


@tweeter.route("/users")
def users():
    query = f"""
    SELECT *
    FROM users
    """

    with engine.connect() as connection:
        users = connection.execute(query).fetchall()

        return render_template("users.html", users=users)

@tweeter.route("/users/<username>")
def user_detail(username):
    user_query = f"""
    SELECT *
    FROM users
    WHERE username='{username}'
    """

    tweets_query = f"""
    SELECT *
    FROM users u
    INNER JOIN tweets t ON u.id=t.user_id
    WHERE u.username='{username}'
    """

    with engine.connect() as connection:
        user = connection.execute(user_query).fetchone()
        tweets = connection.execute(tweets_query).fetchall()

        return render_template(
            "user_detail.html",
            user=user,
            tweets=tweets)


@tweeter.route("/login")
def login():
    return render_template("login.html")

@tweeter.route("/login", methods=["POST"])
def handle_login():
    username = request.form["username"]
    password = request.form["password"]

    query = f"""
    SELECT id, password
    FROM users
    WHERE username='{username}'
    """

    with engine.connect() as connection:
        user = connection.execute(query).fetchone()

        password_matches = check_password_hash(user[1], password)

        if user and password_matches:
            session["username"] = username
            session["user_id"] = user[0]

            return redirect(url_for("index"))

@tweeter.route("/logout")
def logout():
    pass


@tweeter.route("/tweet", methods=["POST"])
def handle_tweet():
    tweet = request.form["tweet"]

    query = f"""
    INSERT INTO tweets(user_id, tweet)
    VALUES ({session["user_id"]}, '{tweet}')
    """

    with engine.connect() as connection:
        connection.execute(query)

        return redirect(url_for("index"))

@tweeter.route("/follow/<followee>")
def follow(followee):
    if "user_id" in session:
        query = f"""
        INSERT INTO follows(follower_id, followee_id)
        VALUES({session["user_id"]}, {followee})
        """

        with engine.connect() as connection:
            connection.execute(query)

            return redirect(url_for("index"))
    else:
        pass

@tweeter.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@tweeter.errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403

tweeter.run(debug=True, port=8080)