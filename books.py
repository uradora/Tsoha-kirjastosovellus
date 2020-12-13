from db import db
import users, genres, authors, lists, reviews

def get_bookcount():
    result = db.session.execute("SELECT COUNT (*) FROM books")
    return result.fetchone()[0]

def get_books():
	result = db.session.execute("SELECT id, name FROM books")
	return result.fetchall()

def get_book(id):
    sql = "SELECT B.name, G.name, A.name, B.publisher, B.published_in, B.year, B.isbn" \
        " FROM books B JOIN genres G ON G.id=B.genre_id JOIN authors A on A.id=B.author_id WHERE B.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send(name,genre,author,publisher,published_in,year,isbn):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT name, id FROM books WHERE LOWER(name)=LOWER(:name)"
    result = db.session.execute(sql, {"name":name})
    book = result.fetchone()
    if book == None:
        if (not name) or (not genre) or (not author) or (not publisher) \
        or (not published_in) or (not year) or (not isbn):
            return False
        genre_id = genres.get_id_byname(genre)
        if genre_id == None:
            genre_id = genres.add_genre(genre)
        else:
            genre_id = genre_id[0]
        author_id = authors.get_id_byname(author)
        if author_id == None:
            author_id = authors.add_author(author)
        else:
            author_id = author_id[0]
        if !(isinstance(year, int)):
            year = None
        sql = "INSERT INTO books (name, author_id, genre_id, publisher, " \
            "published_in, year, isbn) VALUES (:name, :author_id, :genre_id, :publisher, " \
            ":published_in, :year, :isbn)"
        db.session.execute(sql, {"name":name, "author_id":author_id, "genre_id":genre_id,
        "publisher":publisher, "published_in":published_in, "year":year, "isbn":isbn})
        db.session.commit()
        return True
    else:
        return False

def find_byquery(query):
    sql = "SELECT id, name FROM books WHERE LOWER(name) LIKE LOWER(:query)"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def delete_book(id):
    listswithbook = lists.get_lists_with_bookid(id)
    if listswithbook != None:
        if lists.delete_book_fromlist(id) != True:
            return False
    reviewswithbook = reviews.get_reviews_with_bookid(id)
    if reviewswithbook != None:
        if reviews.delete_review_bybook(id) != True:
            return False
    try:
        sql = "DELETE from books WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    except:
        return False

