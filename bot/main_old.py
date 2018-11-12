import sys
import telebot
import sqlite3
from telebot import types

user_scores = {}
true = ""
scores = [0, 100, 200, 300, 500, 1000, 2000, 4000, 6000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

BOT_TOKEN = '662251700:AAGYdnsh6O1TLMWlRK0tSfwt49-nUva00Gg'

if(not BOT_TOKEN):
	sys.exit('Bot token not found')

db = sqlite3.connect("questions.db", check_same_thread=False)
cursor = db.cursor()

bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def start_game(message):
    bot.reply_to(message, "Привіт, " + message.from_user.username + ". Починаємо гру!")
    user_scores[message.from_user.username] = 0
    new_question(message)

def new_question(message):
    cursor.execute("SELECT * FROM questions WHERE rowid=1")
    question = cursor.fetchone()
    global true
    true = question[1]
    bot.send_message(message.chat.id, question[0])
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton(question[1])
    itembtnv = types.KeyboardButton(question[2])
    itembtnc = types.KeyboardButton(question[3])
    itembtnd = types.KeyboardButton(question[4])
    itembtne = types.KeyboardButton('Подсказка')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    markup.row(itembtne)
    msg = bot.send_message(message.chat.id, "Ваша відповідь: ", reply_markup=markup)
    bot.register_next_step_handler(msg, check)

def check(message):
    if(message.from_user.username not in user_scores):
        msg = bot.reply_to(message, "Ви не граєте!")
        bot.register_next_step_handler(msg, check)
    elif(message.text == true):
        if(user_scores[message.from_user.username] != 15):
            user_scores[message.from_user.username] += 1
            bot.send_message(message.chat.id, "Гарна робота! У вас тепер " + str(scores[user_scores[message.from_user.username]]) + " гривень!")
            new_question(message)
        else:
            bot.send_message(message.chat.id, "Вітаю Вас, " + message.from_user.username + "! Ви відповіли на всі 15 запитань!")
    else:
        bot.send_message(message.chat.id, "Вы програли!")
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Гра завершена!", reply_markup=markup)
    user_scores.pop(message.from_user.username)
    
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()
