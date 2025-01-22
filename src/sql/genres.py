from sqlalchemy.sql import text
from app import db

def get():
    command = text("""SELECT G.id, G.name FROM genres G""")
    result = db.session.execute(command)
    return result.fetchall()


def get_genres():
    command = text("""SELECT G.id, G.name 
                      FROM genres G 
                      INNER JOIN movies M ON M.genreid = G.id 
                      GROUP BY G.id""")
    result = db.session.execute(command)
    return result.fetchall()