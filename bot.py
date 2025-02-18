import telebot

from config import Config



bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)



@bot.message_handler(commands=['start'])

def start(message):

    bot.send_message(message.chat.id, "Bot Started!")



bot.polling()
