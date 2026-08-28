from flask import Flask
import sqlite3
from flask import redirect, render_template, request, session, abort, flash
import db
import config
import posts
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@app.route("/home")
def home():
    require_login()
    all_posts = posts.get_posts()
    return render_template("home.html", posts = all_posts)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/home")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id :
            session["user_id"] = user_id
            session["username"] = username
            #session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    #kato virhe ilmoituksia sitten vähä myöhemmin
    if len(username) < 1:
        return "nimi ei sovi"
    if len(password1) < 1:
        return "salasana ei sovi"
    if password1 != password2:
        flash("VIRHE: salasanat eivät täsmää")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")
    return render_template("user_registered.html")

@app.route("/new_post")
def new_item():
    return render_template("uuspost.html")

@app.route("/create_post", methods=["POST"])
def create_item():
    require_login()
    poster_id = session["user_id"]
    title = request.form["title"]
    body = request.form["body"]
    if not title or len(title) > 100 or len(body) > 7000:
        abort(403)

    posts.add_post(poster_id, title, body)
    return redirect("/")

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    return render_template("post.html", post=post)

@app.route("/edit/<int:post_id>")
def edit_post(post_id):
    require_login()
    post = posts.get_post(post_id)

    if not post:
        abort(404)
    if post["poster_id"] != session["user_id"]:
        abort(403)

    return render_template("editpost.html", post=post)

@app.route("/update_post", methods=["POST"])
def update_post():
    require_login()

    post_id = request.form["post_id"]
    post = posts.get_post(post_id)

    if not post:
        abort(404)
    if post["poster_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 100:
        abort(403)
    body = request.form["body"]
    if not body or len(body) > 7000:
        abort(403)

    posts.update_post(post_id, title, body)
    return redirect("/post/" + str(post_id))

@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def remove_post(post_id):
    require_login()
    post = posts.get_post(post_id)

    if not post:
        abort(404)
    if post["poster_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("removepost.html", post=post)

    if request.method == "POST":
        if "continue" in request.form:
            posts.remove_post(post_id)
            return redirect("/home")
        else:
            return redirect("/post/" + str(post_id))

@app.route("/search_posts")
def search_posts():
    query = request.args.get("query")
    if query:
        results = posts.search_posts(query)
    else:
        query = ""
        results = []
    return render_template("search_post.html", query=query, results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    require_login()
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_posts = users.get_posts(user_id)
    return render_template("user_page.html", user=user, posts=user_posts)
