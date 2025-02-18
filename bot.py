import telebot
from config import Config
import requests
import time
import threading
from views_thread import increase_views

bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)
views_thread = None  # Global variable initialize kiya

LOG_GROUP_ID = Config.LOG_GROUP_ID

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Views Bot Started! Commands: /start - Bot start karein /views - Views badhane lag jayega /stop - Views badhane band karein")

@bot.message_handler(commands=['views'])
def views(message):
    global views_thread
    if views_thread is None or not views_thread.is_alive():
        views_thread = threading.Thread(target=increase_views)
        views_thread.daemon = True
        views_thread.start()
        bot.send_message(message.chat.id, "Views increase process started! Bot ko mat band karein.")
    else:
        bot.send_message(message.chat.id, "Views increase process already started!")

@bot.message_handler(commands=['stop'])
def stop(message):
    global views_thread
    if views_thread is not None and views_thread.is_alive():
        views_thread._stop()
        views_thread = None  # Thread ko None kar diya
        bot.send_message(message.chat.id, "Views increase process stopped!")
    else:
        bot.send_message(message.chat.id, "Views increase process already stopped!")

Bot start hone par log group pe message
@bot.message_handler(commands=['start_bot'])
def start_bot(message):
    pass  # Is function ko ignore karein

print("Bot starting...")
try:
    bot.send_message(LOG_GROUP_ID, "Views Bot Started!")
    print("Bot started successfully!")
except Exception as e:
    print(f"Bot start failed: {str(e)}")

bot.polling()
