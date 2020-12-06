from db import db
import users, books

def get_list_byuser(userid):
    sql = "SELECT B.name, L.book_id FROM users U, books B, lists L" \
        " WHERE U.id = L.user_id AND B.id = L.book_id AND L.user_id=:userid"
    result = db.session.execute(sql, {"userid":userid})
    return result.fetchall()

def getbook_fromlist(book_id,userid):
    sql = "SELECT book_id, user_id FROM lists WHERE book_id=:book_id AND user_id=:userid"
    result = db.session.execute(sql, {"book_id":book_id, "userid":userid})
    return result.fetchone()

def addbook_tolist(book_id,userid):
    if userid == 0:
        return False
    try:
        sql = "INSERT INTO lists (user_id, book_id) VALUES (:userid, :book_id)"
        db.session.execute(sql, {"userid":userid,"book_id":book_id})
        db.session.commit()
        return True
    except:
        return False

def get_lists_with_bookid(book_id):
    sql = "SELECT * FROM lists WHERE book_id=:book_id"
    result = db.session.execute(sql, {"book_id":book_id})
    return result.fetchall()

def delete_book_fromlist(book_id):
    try:
        sql = "DELETE FROM lists WHERE book_id=:book_id"
        db.session.execute(sql, {"book_id":book_id})
        db.session.commit()
        return True
    except:
        return False

