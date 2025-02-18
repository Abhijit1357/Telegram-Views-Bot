import requests
import time
import threading
import logging
import random
from proxy_scraper import ProxyScraper
from config import Config
from requests.auth import HTTPProxyAuth

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
        random_proxy = random.choice(proxies_list)
        try:
            proxy_dict = {
                'http': f'http://{random_proxy}',
                'https': f'http://{random_proxy}'
            }
            proxy_auth = HTTPProxyAuth('proxy_username', 'proxy_password')
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(post_url, headers=headers, proxies=proxy_dict, auth=proxy_auth, timeout=10)
            if response.status_code == 200:
                view_counter.increment()
                bot.send_message(message.chat.id, f"Views: {view_counter.get_views()}")
                logging.info(f'Views sent: {view_counter.get_views()}')
            else:
                logging.warning(f'Proxy {random_proxy} blocked or invalid')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error with proxy {random_proxy}: {str(e)}')
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
