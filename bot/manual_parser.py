import sqlite3

db = sqlite3.connect("questions.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS questions (question text, answer text, wrong1 text, wrong2 text, wrong3 text)")
db.commit()
while(True):
    print("Введите вопрос: ")
    question = input()
    print("Введите верный ответ: ")
    answer1 = input()
    print("Введите неверный ответ: ")
    answer2 = input()
    print("Введите неверный ответ: ")
    answer3 = input()
    print("Введите неверный ответ: ")
    answer4 = input()
    cursor.execute("INSERT INTO questions VALUES (?,?,?,?,?)", [question, answer1, answer2, answer3, answer4])
    db.commit()
    print("Для введения ещё одного вопроса введите 1")
    if(input() != "1"):
        break;

db.close()
