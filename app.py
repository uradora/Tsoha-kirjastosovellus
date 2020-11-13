from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

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
	sql = "SELECT password FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		return redirect("/invalid")
	else: 
		hash_value = user[0]
		if check_password_hash(hash_value,password):
			session["username"] = username
			return redirect("/books")
		else:
			return redirect("/invalid")

@app.route("/invalid")
def invalid():
	return render_template("invalid.html")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/newuser")
def newuser():
	return render_template("newuser.html")

@app.route("/senduser", methods=["POST"])
def senduser():
	#what it username exists
	username = request.form["username"]
	password = request.form["password"]
	hash_value = generate_password_hash(password)
	sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
	db.session.execute(sql, {"username":username, "password":hash_value})
	db.session.commit()
	return redirect("/")


@app.route("/books")
def books():
	result = db.session.execute("SELECT COUNT (*) FROM books")
	count = result.fetchone()[0]
	result = db.session.execute("SELECT id, name FROM books")
	books = result.fetchall()
	return render_template("books.html", count=count, books=books)

@app.route("/book/<int:id>")
def book(id):
	result = db.session.execute("SELECT name, genre, author, id FROM books WHERE id=:id", {"id":id})
	book = result.fetchall()
	return render_template("book.html", book=book, id=id)

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
	#what it book exists
	name = request.form["name"]
	genre = request.form["genre"]
	author = request.form["author"]
	sql = "INSERT INTO books (name, genre, author) VALUES (:name, :genre, :author)"
	db.session.execute(sql, {"name":name, "genre":genre, "author":author})
	#author needs to be added to liitostaulu later 
	#and remove author column from books table
	#what if author exists
	#sql = "INSERT INTO authors (name) VALUES (:name)"
	#db.session.execute(sql, {"name":name})
	db.session.commit()
	return redirect("/")

@app.route("/sendreview", methods=["POST"])
def sendreview():
	book_id = request.form["id"]
	review = request.form["review"]
	print(review)
	if "review" in request.form:
		sql = "INSERT INTO reviews (stars, book_id) VALUES (:review, :book_id)"
		db.session.execute(sql, {"review":review, "book_id":book_id})
		db.session.commit()
	return redirect("/book/"+str(book_id))

@app.route("/form")
def form():
	return render_template("form.html")

@app.route("/result")
def result():
	query = request.args["query"]
	sql = "SELECT id, name FROM books WHERE LOWER(name) LIKE LOWER(:query)"
	result = db.session.execute(sql, {"query":"%"+query+"%"})
	books = result.fetchall()
	return render_template("result.html", books=books)
