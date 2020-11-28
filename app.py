from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

def user_id():
	return session.get("user_id",0)

def user_name():
	return session.get("username","")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	sql = "SELECT password, id FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		return redirect("/invalid")
	else: 
		hash_value = user[0]
		if check_password_hash(hash_value,password):
			session["username"] = username
			session["user_id"] = user[1]
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
	username = request.form["username"]
	password = request.form["password"]
	sql = "SELECT password, id FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
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
	username = user_name()
	if username:
		sql = "SELECT id, username FROM users WHERE username=:username"
		user = db.session.execute(sql, {"username":username})
		return render_template("books.html", count=count, books=books, user=user)
	else:
		return redirect("/")

@app.route("/book/<int:id>")
def book(id):
	#aika purkkakoodia
	result = db.session.execute("SELECT name, genre_id, author_id FROM books WHERE id=:id", {"id":id})
	book = result.fetchone()
	genre_id = book[1]
	author_id = book[2]
	sql = "SELECT name FROM genres WHERE id=:genre_id"
	result = db.session.execute(sql, {"genre_id":genre_id})
	if result != None:
		genre = result.fetchone()[0]
	sql = "SELECT name FROM authors WHERE id=:author_id"
	result = db.session.execute(sql, {"author_id":author_id})
	if result != None:
		author = result.fetchone()[0]
	return render_template("book.html", name=book[0], genre=genre, author=author, id=id)

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
	name = request.form["name"]
	genre = request.form["genre"]
	author = request.form["author"]
	sql = "SELECT name, id FROM books WHERE LOWER(name)=LOWER(:name)"
	result = db.session.execute(sql, {"name":name})
	book = result.fetchone()
	if book == None:
		sql = "SELECT id FROM genres WHERE LOWER(name)=LOWER(:genre)"
		result = db.session.execute(sql, {"genre":genre})
		if result != None:
			genre_id = result.fetchone()[0]
		else:
			sql = "INSERT INTO genres (name) VALUES (:genre)"
			db.session.execute(sql, {"genre":genre})
			result = db.session.execute("SELECT currval('genres_id_seq')")
			if result != None:
				genre_id = result.fetchone()[0]
		sql = "SELECT id FROM authors WHERE LOWER(name)=LOWER(:author)"
		result = db.session.execute(sql, {"author":author})
		if result != None:
				author_id = result.fetchone()[0]
		else:
			sql = "INSERT INTO authors (name) VALUES (:author)"
			db.session.execute(sql, {"author":author})
			result = db.session.execute("SELECT currval('authors_id_seq')")
			if result != None:
				author_id = result.fetchone()[0]
		sql = "INSERT INTO books (name, author_id, genre_id) VALUES (:name, :author_id, :genre_id)"
		db.session.execute(sql, {"name":name, "author_id":author_id, "genre_id":genre_id})
		db.session.commit()
	return redirect("/books")

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

@app.route("/booklist/")
def booklist():
	userid = user_id()
	resultbooks = db.session.execute("SELECT name, book_id FROM users U, books B, lists L WHERE U.id = L.user_id AND B.id = L.book_id AND L.user_id=:userid", {"userid":userid})
	books = resultbooks.fetchall()
	return render_template("booklist.html", books=books)

@app.route("/addtolist", methods=["POST"])
def addtolist():
	book_id = request.form["id"]
	username = user_name()
	if username != None:
		sql = "SELECT id FROM users WHERE username=:username"
		result = db.session.execute(sql, {"username":username})
		user_id = result.fetchone()[0]
		sql = "SELECT book_id, user_id FROM lists WHERE book_id=:book_id AND user_id=:user_id"
		result = db.session.execute(sql, {"book_id":book_id, "user_id":user_id})
		#toimii mutta niin paljon purkkaa
		if result != None:
			listing = result.fetchone()
		if listing == None:
			sql = "INSERT INTO lists (user_id, book_id) VALUES (:user_id, :book_id)"
			db.session.execute(sql, {"user_id":user_id, "book_id":book_id})
			db.session.commit()
	return redirect("/book/"+str(book_id))

@app.route("/reviews/<int:id>")
def reviews(id):
	sql = "SELECT stars, COUNT(stars) FROM reviews WHERE book_id=:id GROUP BY stars"
	result = db.session.execute(sql, {"id":id})
	reviews = result.fetchall()
	sql = "SELECT COUNT (*) FROM reviews WHERE book_id=:id"
	result = db.session.execute(sql, {"id":id})
	count = result.fetchone()[0]
	return render_template("reviews.html", reviews=reviews, id=id, count=count)


