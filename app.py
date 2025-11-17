from flask import Flask
import sqlite3
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import posts


app = Flask(__name__)
app.secret_key = config.secret_key


#Etusivu??
@app.route("/")
def index():
    all_posts = posts.get_posts()
    return render_template("index.html", posts = all_posts)


#Tunnuksen luonti
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat/täsmää"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


#########################################################################
#täs on nyt toi index.html ja login.html molemmat
#login.html ei taida rn tehä mitää ja salee tuli vaa vahingos kopsattuu kahesti
#mut emt ehk sit tekee viä jotai
#tää nyt jääkööt täl kertaa bäckburnerille


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username]) [0]
    user_id = result["id"]
    password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")



#Uuden postauksen luominen
@app.route("/new_item")
def new_item():
    return render_template("uuspost.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    poster_id = session["user_id"]
    title = request.form["title"]
    body = request.form["body"]

    posts.add_post(poster_id, title, body)

    return redirect("/")

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)