import telebot
from config import Config

#Bot ko initialize karna
bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

#/start command ka handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Welcome to my bot!")

#/help command ka handler
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "This bot can help you with...")

#Message ka handler
@bot.message_handler(content_types=['text'])
def handle_message(message):
    bot.send_message(message.chat.id, "You said: " + message.text)

#Bot ko start karna
bot.polling()
