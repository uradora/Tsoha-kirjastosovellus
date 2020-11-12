from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
	return render_template("index.html")
	
@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	session["username"] = username
	return redirect("/books")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/books")
def books():
	result = db.session.execute("SELECT COUNT (*) FROM books")
	count = result.fetchone()[0]
	result = db.session.execute("SELECT name FROM books")
	books = result.fetchall()
	return render_template("books.html", count=count, books=books)

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
	name = request.form["name"]
	sql = "INSERT INTO books (name) VALUES (:name)"
	db.session.execute(sql, {"name":name})
	db.session.commit()
	return redirect("/")

@app.route("/form")
def form():
	return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
	return render_template("result.html", book=request.form["book"])
