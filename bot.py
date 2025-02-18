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

@bot.message_handler(commands=['views'])
def views(message):
    threading.Thread(target=start_views_thread, args=(bot, message)).start()

if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        print("Error: " + str(e))
