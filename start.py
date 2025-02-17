import os
from telegram_views_bot import bot

if __name__ == '__main__':
    print("Telegram Views Bot Starting... Version 1.0")

    # Environment Variables se config load karna
    try:
        bot.token = os.environ['TELEGRAM_BOT_TOKEN']
        bot.config.TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
        bot.config.TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
        bot.config.CHANNEL_USERNAME = os.environ['CHANNEL_USERNAME']
        bot.config.POST_ID = os.environ['POST_ID']
    except KeyError as e:
        print(f"Environment Variable nahin mili: {e}")
        print("Config.py se config load karta hoon.")

    # Bot ko start karna
    bot.polling()
    print("Telegram Views Bot Started Successfully! Version 1.0")
