from flask import make_response
from db import db

def add(name, description, data, genreid):
    command = """INSERT INTO movies (name, description, cover, genreid) VALUES (:name, :description, :cover, :genreid) RETURNING id"""
    index = db.session.execute(command, {
        "name": name, "description": description, "cover": data, "genreid": genreid})
    db.session.commit()
    return index.fetchone()[0]


def get_all():
    command = """SELECT M.id, M.name, M.description, G.name AS genre, CAST(ROUND(AVG(R.stars)) AS INT) as reviews FROM movies 
    M LEFT JOIN reviews R ON M.id=R.movieid LEFT JOIN genres G ON G.id = M.genreid LEFT JOIN requests Q ON Q.movieid = M.id 
    WHERE Q.movieid IS NULL GROUP BY M.id, G.name ORDER BY M.id DESC"""
    result = db.session.execute(command)
    return result.fetchall()


def get_genre(id):
    command = """SELECT M.id, M.name, M.description, CAST(ROUND(AVG(R.stars)) AS INT) as reviews FROM movies M LEFT JOIN reviews 
    R ON M.id=R.movieid LEFT JOIN requests Q ON Q.movieid = M.id WHERE Q.movieid IS NULL AND M.genreid=:genreid GROUP BY M.id 
    ORDER BY M.id DESC"""
    result = db.session.execute(command, {"genreid": id})
    return result.fetchall()


def get_requested():
    command = """SELECT M.id, M.name, M.description, G.name AS genre FROM movies M LEFT JOIN genres G ON G.id = M.genreid 
    INNER JOIN requests Q ON Q.movieid = M.id GROUP BY M.id, G.name ORDER BY M.id DESC"""
    result = db.session.execute(command)
    return result.fetchall()


def search(query):
    command = """SELECT M.id, M.name, M.description, G.name AS genre, CAST(ROUND(AVG(R.stars)) AS INT) as reviews FROM movies 
    M LEFT JOIN reviews R ON M.id=R.movieid LEFT JOIN genres G ON G.id = M.genreid LEFT JOIN requests Q ON Q.movieid = M.id 
    WHERE Q.movieid IS NULL AND LOWER(M.name) LIKE LOWER(:query) OR LOWER(M.description) LIKE LOWER(:query) GROUP BY M.id, 
    G.name ORDER BY M.id DESC"""
    result = db.session.execute(command, {"query": f"%{query}%"})
    return result.fetchall()


def get_one(id):
    command = """SELECT M.id, M.name, M.description, G.name AS genre, CAST(ROUND(AVG(R.stars)) AS INT) as reviews FROM movies 
    M LEFT JOIN genres G ON G.id = M.genreid LEFT JOIN reviews R ON M.id=R.movieid LEFT JOIN requests Q ON Q.movieid = M.id 
    WHERE Q.movieid IS NULL AND M.id=:movie GROUP BY M.id, G.name"""
    result = db.session.execute(command, {"movie": id})
    return result.fetchone()


def get_cover(id):
    result = db.session.execute(
        "SELECT cover FROM movies WHERE id=:id", {"id": id})
    if data := result.fetchone():
        response = make_response(bytes(data[0]))
        response.headers.set("Content-Type", "image/jpeg")
        return response
    return False


def delete(id):
    db.session.execute("""DELETE FROM reviews WHERE movieid=:id""", {"id": id})
    if db.session.execute("""DELETE FROM movies WHERE id=:id""", {"id": id}):
        db.session.commit()
    return True
