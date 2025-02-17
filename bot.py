import telebot 
from config import Config 
import requests 
import time 
import threading 
from views_thread import increase_views 
 
bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN) 
 
@bot.message_handler(commands=['start']) 
def start(message): 
  bot.send_message(message.chat.id, "Views Bot Started!") 
 
@bot.message_handler(commands=['views']) 
def views(message): 
  global views_thread 
  views_thread = threading.Thread(target=increase_views) 
  views_thread.start() 
