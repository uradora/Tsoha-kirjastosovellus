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
	sql = "SELECT id FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	if not result:
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
	result = db.session.execute("SELECT name, genre, author, id FROM books WHERE id=:id", {"id":id})
	book = result.fetchall()
	return render_template("book.html", book=book, id=id)

@app.route("/new")
def new():
	return render_template("new.html")

@app.route("/send", methods=["POST"])
#kirjan lisääminen ei toimi
def send():
	#what it book exists, test if that validation works
	name = request.form["name"]
	genre = request.form["genre"]
	author = request.form["author"]
	sql = "SELECT id FROM books WHERE LOWER(name)=LOWER(:name)"
	result = db.session.execute(sql, {"name":name})
	if result:
		flash('Kirja on jo lisätty')
	else:
		#tuleeko error jos ei löy'y
		#test with a new genre
		sql = "SELECT id FROM genres WHERE LOWER(name)=LOWER(:genre)"
		genre_id = db.session.execute(sql, {"genre":genre})
		if not genre_id:
			#tulee kahdesti sama kysely
			sql = "INSERT INTO genres (name) VALUES (:genre)"
			db.session.execute(sql, {"genre":genre})
			sql = "SELECT id FROM genres WHERE LOWER(name)=LOWER(:genre)"
			genre_id = db.session.execute(sql, {"genre":genre})
		sql = "SELECT id FROM authros WHERE LOWER(name)=LOWER(:author)"
		author_id = db.session.execute(sql, {"author":author})
		if not author_id:
			sql = "INSERT INTO authors (name) VALUES (:author)"
			db.session.execute(sql, {"author":author})
			sql = "SELECT id FROM authors WHERE LOWER(name)=LOWER(:author)"
			author_id = db.session.execute(sql, {"author":author})
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
	if username:
		sql = "SELECT id FROM users WHERE username=:username"
		user_id = db.session.execute(sql, {"username":username})
		sql = "INSERT INTO lists (user_id, book_id) VALUES (:user_id, :book_id)"
		db.session.execute(sql, {"user_id":user_id, "book_id":book_id})
		db.session.commit()
	return redirect("/book/"+str(book_id))

