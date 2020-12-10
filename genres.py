from db import db

#maybe delete
def get_genre(id):
    sql = "SELECT name FROM genres WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_id_byname(name):
    sql = "SELECT id FROM genres WHERE LOWER(name)=LOWER(:name)"
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()

def add_genre(name):
    sql = "INSERT INTO genres (name) VALUES (:name) RETURNING id"
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()[0]