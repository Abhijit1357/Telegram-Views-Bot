import telebot

from config import Config

import requests

import time

import threading

from views_thread import increase_views



bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)



@bot.message_handler(commands=['start'])

def start(message):

    bot.send_message(message.chat.id, "Views Bot Started! 

Commands: 

/start - Bot start karein 

/views - Views badhane lag jayega

@stop - Views badhane band karein")



@bot.message_handler(commands=['views'])

def views(message):

    global views_thread

    views_thread = threading.Thread(target=increase_views)

    views_thread.daemon = True

    views_thread.start()

    bot.send_message(message.chat.id, "Views increase process started! 

Bot ko mat band karein.")



@bot.message_handler(commands=['stop'])

def stop(message):

    global views_thread

    if views_thread.is_alive():

        views_thread._stop()

        bot.send_message(message.chat.id, "Views increase process stopped!")

    else:

        bot.send_message(message.chat.id, "Views increase process already stopped!")



bot.polling()
