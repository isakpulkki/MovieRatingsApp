import os
from sqlalchemy.sql import text
from app import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(name, password):
    command = text("SELECT password, id, admin FROM users WHERE name = :name")
    result = db.session.execute(command, {"name": name})
    user = result.fetchone()
    if not user:
        return False, "user"
    if not check_password_hash(user[0], password):
        return False, "password"
    session["user_id"] = user[1]
    session["user_name"] = name
    session["user_admin"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True, ""

def register(username, password):
    command = text("""INSERT INTO users (name, password, admin) 
                      VALUES (:name, :password, False)""")
    db.session.execute(command, {"name": username, "password": generate_password_hash(password)})
    db.session.commit()
    return True

def username_available(name):
    command = text("""SELECT * FROM users WHERE LOWER(name) = LOWER(:name)""")
    result = db.session.execute(command, {"name": name})
    return result.fetchone()

def change_password(oldpassword, password):
    command = text("SELECT password FROM users WHERE id = :userid")
    result = db.session.execute(command, {"userid": get_user_id()})
    user = result.fetchone()
    if not check_password_hash(user[0], oldpassword):
        return False
    command = text("UPDATE users SET password = :password WHERE id = :userid")
    db.session.execute(
        command, {"userid": get_user_id(), "password": generate_password_hash(password)})
    db.session.commit()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_admin"]

def get_user_id():
    return session.get("user_id", 0)

def get_admin():
    return session.get("user_admin")

def get_username():
    return session.get("user_name")

def check_csrf():
    return session.get("csrf_token")