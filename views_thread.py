import requests
import time
import threading
import logging
import random
from proxy_scraper import ProxyScraper
from config import Config
from telegram.ext import CommandHandler, MessageHandler, Updater
import concurrent.futures

logging.basicConfig(level=logging.INFO)

class ViewCounter:
    def __init__(self):
        self.views = 0

    def increment(self):
        self.views += 1

    def get_views(self):
        return self.views

view_counter = ViewCounter()

def send_view(bot, message, post_url, proxy):
    try:
        proxy_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(post_url, headers=headers, proxies=proxy_dict, timeout=30)
        if response.status_code == 200:
            view_counter.increment()
            bot.send_message(message.chat.id, f"Views: {view_counter.get_views()}")
            logging.info(f'Views sent: {view_counter.get_views()}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error with proxy {proxy}: {str(e)}')

def increase_views(bot, message, post_url):
    proxy_scraper = ProxyScraper()
    max_views = Config.MAX_VIEWS_PER_INTERVAL
    views_sending_interval = Config.VIEWS_SENDING_INTERVAL
    while view_counter.get_views() < max_views:
        proxies_list = proxy_scraper.collect_proxies()
        if not proxies_list:
            logging.error('No proxies available')
            break
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda proxy: send_view(bot, message, post_url, proxy), proxies_list)
        time.sleep(views_sending_interval)
        logging.info('Views sending limit reached or completed')
    bot.send_message(message.chat.id, "Views increased!")

def handle_proxies_command(bot, update):
    try:
        with open('proxies.txt', 'r') as f:
            proxies = f.read()
        bot.send_message(update.message.chat.id, proxies)
    except FileNotFoundError:
        bot.send_message(update.message.chat.id, "Proxies file not found")

def start_views_thread(bot, update):
    if update.reply_to_message:
        post_url = update.reply_to_message.text
    else:
        text = update.text.split(' ')
        if len(text) > 1:
            post_url = text[1]
        else:
            bot.send_message(update.effective_chat.id, "Invalid command. Please provide a URL or reply to a message.")
            return
    if update.text.startswith('/proxies'):
        handle_proxies_command(bot, update)
    else:
        threading.Thread(target=increase_views, args=(bot, update, post_url)).start()

def main():
    updater = Updater(token=Config.TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start_views', start_views_thread))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
