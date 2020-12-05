from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def user_id():
	return session.get("user_id",0)

def is_admin():
    userid = user_id()
    if userid == 0:
        return False
    else:
        sql = "SELECT admin FROM users WHERE id=:userid"
        result = db.session.execute(sql, {"userid":userid})
        admin = result.fetchone()
        if admin != None:
            return admin[0]
        else:
            return False

def is_loggedin():
    userid = user_id

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = username
            return True
        else:
            return False
    
def logout():
    del session["user_id"]
    del session["username"]

def register(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        hash_value = generate_password_hash(password)
        try:
            sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,'f')"
            db.session.execute(sql, {"username":username,"password":hash_value})
            db.session.commit()
        except:
            return False
        return login(username,password)
    else:
        return False




    

