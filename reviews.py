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
    userid = users.user_id()
    if userid == 0:
        return False
    sql = "SELECT 1 FROM reviews WHERE user_id=:userid and book_id=:book_id"
    result = db.session.execute(sql, {"userid":userid, "book_id":book_id})
    if result.fetchone() == None:
        try:
            if int(review) > 0 and int(review) < 6:
                sql = "INSERT INTO reviews (stars, book_id, user_id) VALUES (:review, :book_id, :userid)"
                db.session.execute(sql, {"review":review, "book_id":book_id, "userid":userid})
                db.session.commit()
                return True
            else:
                return False
        except:
            return False
    else:
        try:
            sql = "UPDATE reviews SET stars = :review WHERE user_id=:userid"
            result = db.session.execute(sql, {"review":review, "userid":userid})
            db.session.commit()
            return True
        except:
            return False




