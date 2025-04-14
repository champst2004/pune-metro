import mysql.connector
from credentials import passw

def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=passw,
        database="punemetro"
    )
    cursor = db.cursor(dictionary=True)
    return db, cursor
