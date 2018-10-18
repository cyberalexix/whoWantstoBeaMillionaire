import sys
import telebot
from telebot import types

try:
    configFile = open("bot_token.txt", "r")
    BOT_TOKEN = configFile.read()
    configFile.close()
except:
    print("File does not exists or it is not accessible")
    sys.exit(0)


bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, " + message.from_user.username)
    bot.send_message(message.chat.id, "Кто убил Пушкина?")
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Дантес')
    itembtnv = types.KeyboardButton('Д\'Артаньян')
    itembtnc = types.KeyboardButton('Дерипаска')
    itembtnd = types.KeyboardButton('Дункерк')
    itembtne = types.KeyboardButton('Подсказка')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    markup.row(itembtne)
    bot.send_message(message.chat.id, "Ваш ответ: ", reply_markup=markup)

    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, message, reply_markup=markup)

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.from_user.username)

bot.polling()
