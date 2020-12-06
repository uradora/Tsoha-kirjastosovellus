from app import app
import users, books, genres, authors, lists, reviews
from flask import redirect, render_template, request, session

@app.route("/")
def index():
    count = books.get_bookcount()
    bookslist = books.get_books()
    admin = users.is_admin()
    return render_template("index.html", count=count, books=bookslist, admin=admin)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/book/<int:id>")
def book(id):
    book = books.get_book(id)
    genre = genres.get_genre(book[1])[0]
    author = authors.get_author(book[2])[0]
    admin = users.is_admin()
    return render_template("book.html", name=book[0], genre=genre, author=author, id=id, admin=admin)

@app.route("/new")
def new():
    if users.is_admin():
	    return render_template("new.html")
    else: return render_template("error.html",message="Ei oikeutta nähdä sivua")

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    genre = request.form["genre"]
    author = request.form["author"]
    if users.is_admin():        
        if books.send(name,genre,author):
            return redirect("/")
        else:
            return render_template("error.html",message="Kirjan lisääminen ei onnistunut")
    else:
        return render_template("error.html",message="Ei oikeutta tehdä tätä toimintoa")

@app.route("/reviews/<int:id>")
def reviewsit(id):
    book = books.get_book(id)
    name = book[0]
    reviewsit = reviews.get_reviews(id)
    count = reviews.get_count(id)
    if count == None:
        count = 0
    else:
        count = count[0]
    return render_template("reviews.html", reviews=reviewsit, id=id, count=count, name=name)

@app.route("/sendreview", methods=["POST"])
def sendreview():
    book_id = request.form["id"]
    review = request.form["review"]
    if "review" in request.form:
        if reviews.send_review(review,book_id):
            return redirect("/book/"+str(book_id))
        else:
            return render_template("error.html",message="Arvostelun lisääminen ei onnistunut")
    else:
        return render_template("error.html",message="Arvostelun lisääminen ei onnistunut")

@app.route("/result")
def result():
    query = request.args["query"]
    bookslist = books.find_byquery(query)
    return render_template("result.html", books=bookslist, query=query)

@app.route("/booklist/")
def booklist():
    userid = users.user_id()
    if userid == 0:
        return render_template("error.html",message="Et ole kirjautunut sisään")
    resultbooks = lists.get_list_byuser(userid)
    return render_template("booklist.html", books=resultbooks)

@app.route("/addtolist", methods=["POST"])
def addtolist():
    book_id = request.form["id"]
    userid = users.user_id()
    #listing = lists.get_list_byuser(userid)
    #if listing != None:
    book = lists.getbook_fromlist(book_id,userid)
    if book == None:
        if lists.addbook_tolist(book_id,userid):
            return redirect("/book/"+str(book_id))
        else:
            return render_template("error.html",message="Kirjan lisääminen listaan epäonnistui")
    else:
        return render_template("error.html",message="Kirja on jo listalla")

@app.route("/deletebook", methods=["POST"])
def deletebook():
    if users.is_admin():
        book_id = request.form["id"]
        if books.delete_book(book_id):
            return redirect("/")
        else:
            return render_template("error.html",message="Kirjan poistaminen ei onnistunut")
    else:
        return render_template("error.html",message="Ei oikeuksia poistaa kirjaa")
        