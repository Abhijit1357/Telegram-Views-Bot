import requests
import time
import threading
import logging
import random
from proxy_scraper import ProxyScraper
from config import Config

logging.basicConfig(level=logging.INFO)

class ViewCounter:
    def __init__(self):
        self.views = 0

    def increment(self):
        self.views += 1

    def get_views(self):
        return self.views

view_counter = ViewCounter()

def increase_views(bot, message, post_url):
    proxy_scraper = ProxyScraper()
    proxies_list = proxy_scraper.collect_proxies()
    max_views = Config.MAX_VIEWS_PER_INTERVAL

    while view_counter.get_views() < max_views:
        for proxy in proxies_list:
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
                response = requests.get(post_url, headers=headers, proxies=proxy_dict, timeout=10)
                if response.status_code == 200:
                    view_counter.increment()
                    bot.send_message(message.chat.id, f"Views: {view_counter.get_views()}")
                    logging.info(f'Views sent: {view_counter.get_views()}')
                    break
                else:
                    logging.warning(f'Proxy {proxy} blocked or invalid')
            except requests.exceptions.RequestException as e:
                logging.error(f'Error with proxy {proxy}: {str(e)}')
                proxies_list.remove(proxy)
                logging.info(f'Proxy {proxy} removed from list')
        if not proxies_list:
            logging.error('No more proxies available')
            proxy_scraper = ProxyScraper()
            proxies_list = proxy_scraper.collect_proxies()
            logging.info('New proxies collected')
        time.sleep(Config.VIEWS_SENDING_INTERVAL)
    logging.info('Views sending limit reached or completed')
    bot.send_message(message.chat.id, "Views increased!")

def start_views_thread(bot, message):
    if message.reply_to_message:
        post_url = message.reply_to_message.text
    else:
        text = message.text.split(' ')
        if len(text) > 1:
            post_url = text[1]
        else:
            bot.send_message(message.chat.id, "Invalid command. Please provide a URL or reply to a message.")
            return
    threading.Thread(target=increase_views, args=(bot, message, post_url)).start()

def handle_proxies_command(bot, message):
    try:
        with open('proxies.txt', 'r') as f:
            proxies = f.read()
            bot.send_message(message.chat.id, proxies)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Proxies file not found")

#Add command handler
bot.add_command('/proxies', handle_proxies_command)
