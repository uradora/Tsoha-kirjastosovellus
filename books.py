from db import db
import users, genres, authors

def get_bookcount():
    result = db.session.execute("SELECT COUNT (*) FROM books")
    return result.fetchone()[0]

def get_books():
	result = db.session.execute("SELECT id, name FROM books")
	return result.fetchall()

def get_book(id):
    sql = "SELECT name, genre_id, author_id FROM books WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send(name,genre,author):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT name, id FROM books WHERE LOWER(name)=LOWER(:name)"
    result = db.session.execute(sql, {"name":name})
    book = result.fetchone()
    if book == None:
        if not name:
            return False
        if not genre:
            return False
        if not author:
            return False
        genre_id = genres.get_id_byname(genre)
        if genre_id == None:
            genre_id = genres.add_genre(genre)
        author_id = authors.get_id_byname(author)
        if author_id == None:
            author_id = authors.add_author(author)
        sql = "INSERT INTO books (name, author_id, genre_id) VALUES (:name, :author_id, :genre_id)"
        db.session.execute(sql, {"name":name, "author_id":author_id, "genre_id":genre_id})
        db.session.commit()
        return True
    else:
        return False

def find_byquery(query):
    sql = "SELECT id, name FROM books WHERE LOWER(name) LIKE LOWER(:query)"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

