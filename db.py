import mysql.connector
from credentials import passw
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=passw,
    database="metro"
)

cursor = db.cursor(dictionary=True)  # Fetch data as dictionaries
