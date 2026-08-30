from flask import Flask
import sqlite3
from flask import redirect, render_template, request, session, abort, flash
import secrets

import db
import config
import posts
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/home")
def home():
    require_login()
    all_posts = posts.get_posts()
    return render_template("home.html", posts = all_posts)

@app.route("/")
def index():
    return render_template("index.html")

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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/home")
        else:
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

    if len(username) < 1:
        return "VIRHE: nimi ei sovi"
    if len(password1) < 5:
        return "VIRHE: salasana ei sovi"
    if password1 != password2:
        return "VIRHE: salasanat eivät täsmää"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return render_template("user_registered.html")

#Posts
@app.route("/new_post")
def new_post():
    require_login()
    classes = posts.get_all_classes()
    return render_template("uuspost.html", classes=classes)

@app.route("/create_post", methods=["POST"])
def create_post():
    require_login()
    check_csrf()

    poster_id = session["user_id"]
    title = request.form["title"]
    if not title or len(title) > 100:
            abort(403)
    body = request.form["body"]
    if not body or len(body) > 7000:
        abort(403)

    #testauusss
    classes = request.form.getlist("classes")
    print(classes)

    all_classes = posts.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_name, class_value = entry.split(":")
            if class_name not in all_classes:
                abort(403)
            if class_value not in all_classes[class_name]:
                abort(403)
            classes.append((class_name, class_value))

    posts.add_post(poster_id, title, body, classes)
    return redirect("/home")

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    classes = posts.get_post_classes(post_id)
    comments = posts.get_comments(post_id)

    return render_template("post.html", post=post, comments=comments, classes=classes)

@app.route("/edit/<int:post_id>")
def edit_post(post_id):
    require_login()
    post = posts.get_post(post_id)

    if not post:
        abort(404)
    if post["poster_id"] != session["user_id"]:
        abort(403)
    
    all_classes = posts.get_all_classes()
    classes = {}
    for post_class in all_classes:
        classes[post_class] = ""
    for entry in posts.get_post_classes(post_id):
        classes[entry["name"]] = entry["value"]

    return render_template("editpost.html", post=post, classes=classes, all_classes=all_classes)

@app.route("/update_post", methods=["POST"])
def update_post():
    require_login()
    check_csrf()

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

    all_classes = posts.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_name, class_value, = entry.split(":")
            if class_name not in all_classes:
                abort(403)
            if class_value not in all_classes[class_name]:
                abort(403)
            classes.append((class_name, class_value))

    posts.update_post(post_id, title, body, classes)
    return redirect("/post/" + str(post_id))

@app.route("/save_post", methods=["POST"])
def save_post(post_id):
    require_login()
    check_csrf()

    post = posts.get_post(post_id)
    if post["poster_id"] == session["user_id"]:
        return "Omat julkaisusi näkyvät aina sivuillasi"
    if not post:
        abort(404)

    saver_id = session["user_id"]
    posts.save_post(post_id, saver_id)
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
        check_csrf()
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

#Commenting on posts
@app.route("/new_comment", methods=["POST"])
def new_comment():
    require_login()
    check_csrf()

    commenter_id = session["user_id"]
    post_id = request.form["post_id"]
    comment = request.form["comment"]
    if not comment or len(comment) > 1000:
        abort(403)

    try:
        posts.add_comment(commenter_id, post_id, comment)
    except sqlite3.IntegrityError:
        abort(403)
    return redirect("/post/" + str(post_id))
