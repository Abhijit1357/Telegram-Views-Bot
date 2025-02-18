import telebot
import threading
from config import Config
from views_thread import start_views_thread
from flask import Flask

app = Flask(__name__)
bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

@app.route('/')
def index():
    return 'Hello, World!'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Welcome to my bot!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "This bot can help you with...")

@bot.message_handler(commands=['views'])
def views(message):
    threading.Thread(target=start_views_thread, args=(bot, message)).start()

if __name__ == '__main__':
    import threading
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000, 'use_reloader': False}).start()
    bot.polling()
