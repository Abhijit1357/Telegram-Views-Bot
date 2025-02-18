import telebot
from config import Config
from views_thread import start_views_thread

bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Welcome to my bot!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "This bot can help you with...")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    bot.send_message(message.chat.id, "You said: " + message.text)

@bot.edited_message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def error_handler(message):
    try:
        bot.send_message(message.chat.id, "You said: " + message.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Error: " + str(e))

def start_views_thread():
    bot.message_handler(commands=['views'])(handle_views_command)

if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        print("Error: " + str(e))
