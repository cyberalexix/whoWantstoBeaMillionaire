import sqlite3

db = sqlite3.connect("questions.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM questions WHERE rowid = 1")
print(cursor.fetchall())
