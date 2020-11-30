from db import db
import users, genres, authors

def get_reviews(id):
    sql = "SELECT stars, COUNT(stars) FROM reviews WHERE book_id=:id GROUP BY stars"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_count(id):
    sql = "SELECT COUNT (*) FROM reviews WHERE book_id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send_review(review,book_id):
    try:
        sql = "INSERT INTO reviews (stars, book_id) VALUES (:review, :book_id)"
        db.session.execute(sql, {"review":review, "book_id":book_id})
        db.session.commit()
        return True
    except:
        return False





