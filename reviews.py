from db import db
import users


def add(description, stars, movieid):
    command = """INSERT INTO reviews (description, stars, userid, movieid, date) VALUES (:description, :stars, :userid, :movieid, NOW())"""
    db.session.execute(command, {"description": description, "stars": stars,
                       "userid": users.get_user_id(), "movieid": movieid})
    db.session.commit()
    return True


def get_movie_reviews(movieid):
    command = """SELECT R.id, R.description, R.stars, R.date, U.name as username FROM reviews R LEFT JOIN users U ON U.id=R.userid WHERE R.movieid=:movieid ORDER BY R.id DESC"""
    result = db.session.execute(command, {"movieid": movieid})
    return result.fetchall()


def get_user_review(movieid):
    command = """SELECT id, description, date, stars FROM reviews WHERE movieid=:movieid AND userid=:userid"""
    result = db.session.execute(
        command, {"movieid": movieid, "userid": users.get_user_id()})
    return result.fetchone()


def get_average(movieid):
    result = db.session.execute(
        """SELECT AVG(stars) FROM reviews WHERE movieid=:movieid""", {"movieid": movieid})
    return result.fetchall()


def delete(id):
    if not users.get_admin():
        command = """DELETE FROM reviews WHERE id=:reviewid AND userid=:userid"""
        if db.session.execute(command, {"reviewid": id, "userid": users.get_user_id()}):
            db.session.commit()
            return True
    else:
        if db.session.execute("""DELETE FROM reviews WHERE id=:reviewid""", {"reviewid": id}):
            db.session.commit()
            return True
    return False
