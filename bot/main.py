import sys
import telebot
import sqlite3
from telebot import types

BOT_TOKEN = ''

if(not BOT_TOKEN):
	sys.exit('Bot token not found')

db = sqlite3.connect("questions.db", check_same_thread=False)
cursor = db.cursor()

def add_log(msg):
    log_file = open('log.txt', mode="a")
    log_file.write(msg + "\n\n")
    log_file.close()
    

bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    if(message.from_user.username.lower() not in ["alexix1234"]):
        bot.send_message(message.chat.id, "Вы не являетесь авторизированным пользователем")
        add_log("User " + message.from_user.username + " tried to add a question!")
        return
    msg = bot.send_message(message.chat.id, """Введите вопрос и ответы в следующем формате:\nВопрос\nПравильный ответ\nНеверный ответ\nНеверный ответ\nНеверный ответ""")
    bot.register_next_step_handler(msg, check)

def check(message):
    if(not message.text):
        bot.send_message(message.chat.id, "Пустое сообщение")
        return
    massive = message.text.split("\n")
    if(len(massive) % 5 != 0):
        bot.send_message(message.chat.id, "Недостаточно строк или некорректный формат!")
        return
    for i in massive:
        if(not i):
            bot.send_message(message.chat.id, "Одно из полей является пустым")
            return
    if(len(massive) == 5):
        add_log("User " + message.from_user.username + " has added folowing question: \nQuestion:'{}'\nTrue answer:{}\nWrong answer:{}\nWrong answer:{}\nWrong answer:{}".format(massive[0], massive[1], massive[2], massive[3], massive[4]))
        cursor.execute("INSERT INTO 'questions' VALUES ('{}', '{}', '{}', '{}', '{}')".format(massive[0], massive[1], massive[2], massive[3], massive[4]))
        bot.send_message(message.chat.id, """Вы добавили следующий вопрос:\nВопрос:'{}'\nПравильный ответ:{}\nНеверный ответ:{}\nНеверный ответ:{}\nНеверный ответ:{}""".format(massive[0], massive[1], massive[2], massive[3], massive[4]))
        db.commit()
    else:
        for i in range(0, len(massive) // 5):
            add_log("User " + message.from_user.username + " has added folowing question: \nQuestion:'{}'\nTrue answer:{}\nWrong answer:{}\nWrong answer:{}\nWrong answer:{}".format(massive[0+(5*i)], massive[1+(5*i)], massive[2+(5*i)], massive[3+(5*i)], massive[4+(5*i)]))
            cursor.execute("INSERT INTO 'questions' VALUES ('{}', '{}', '{}', '{}', '{}')".format(massive[0+(5*i)], massive[1+(5*i)], massive[2+(5*i)], massive[3+(5*i)], massive[4+(5*i)]))
            bot.send_message(message.chat.id, """Вы добавили следующий вопрос:\nВопрос:'{}'\nПравильный ответ:{}\nНеверный ответ:{}\nНеверный ответ:{}\nНеверный ответ:{}""".format(massive[0+(5*i)], massive[1+(5*i)], massive[2+(5*i)], massive[3+(5*i)], massive[4+(5*i)]))
            db.commit()
                            
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()
