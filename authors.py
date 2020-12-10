from db import db

#maybe delete
def get_author(id):
    sql = "SELECT name FROM authors WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_id_byname(name):
    sql = "SELECT id FROM authors WHERE LOWER(name)=LOWER(:name)"
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()

def add_author(name):
    sql = "INSERT INTO authors (name) VALUES (:name) RETURNING id"
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()[0]