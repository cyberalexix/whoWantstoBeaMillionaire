import sqlite3

db = sqlite3.connect("questions.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM questions")
print(cursor.fetchall())
