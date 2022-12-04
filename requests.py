from db import db
import users


def add(movieid):
    command = """INSERT INTO requests VALUES (:userid, :movieid)"""
    db.session.execute(
        command, {"userid": users.get_user_id(), "movieid": movieid})
    db.session.commit()
    return True


def get_user_request():
    command = """SELECT * FROM requests WHERE userid=:userid"""
    value = db.session.execute(command, {"userid": users.get_user_id()})
    return value.fetchall()


def get_movie_request(movieid):
    command = """SELECT * FROM requests WHERE movieid=:movieid"""
    value = db.session.execute(command, {"movieid": movieid})
    return value.fetchone()

def delete(movieid):
    command = """DELETE FROM requests WHERE movieid=:movieid"""
    db.session.execute(command, {"movieid": movieid})
    db.session.commit()
    return True
