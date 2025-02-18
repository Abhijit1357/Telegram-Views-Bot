import telebot
import threading
import logging
from config import Config
from views_thread import start_views_thread
from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

@app.route('/')
def index():
    return 'Hello, World!'

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, "Hello! Welcome to my bot!")
    except Exception as e:
        logging.error(f"Error sending start message: {str(e)}")

@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.send_message(message.chat.id, "This bot can help you with...")
    except Exception as e:
        logging.error(f"Error sending help message: {str(e)}")

@bot.message_handler(commands=['views'])
def views(message):
    try:
        threading.Thread(target=start_views_thread, args=(bot, message)).start()
        bot.send_message(message.chat.id, "Views thread started!")
    except Exception as e:
        bot.send_message(message.chat.id, "Error starting views thread!")
        logging.error(f"Error starting views thread: {str(e)}")

if __name__ == '__main__':
    import threading
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000, 'use_reloader': False}).start()
    bot.polling()
