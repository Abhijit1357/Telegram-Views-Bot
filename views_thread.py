import requests
import time
import threading
import logging
import random
from proxy_scraper import ProxyScraper
from config import Config

logging.basicConfig(level=logging.INFO)

def increase_views(bot, message):
    proxy_scraper = ProxyScraper()
    proxies_list = proxy_scraper.collect_proxies()
    views_sent = 0
    max_views = Config.MAX_VIEWS_PER_INTERVAL

    while views_sent < max_views:
        random_proxy = random.choice(proxies_list)
        try:
            proxy_dict = {
                'http': f'http://{random_proxy}',
                'https': f'http://{random_proxy}'
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
            url = f'https://t.me/{Config.CHANNEL_USERNAME}/{Config.POST_ID}'
            response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
            if response.status_code == 200:
                views_sent += 1
                logging.info(f'Views sent: {views_sent}')
            else:
                logging.warning(f'Proxy {random_proxy} blocked or invalid')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error with proxy {random_proxy}: {str(e)}')
        if views_sent >= max_views:
            break
        time.sleep(Config.VIEWS_SENDING_INTERVAL)
    logging.info('Views sending limit reached or completed')
    bot.send_message(message.chat.id, "Views increased!")

def start_views_thread(bot, message):
    threading.Thread(target=increase_views, args=(bot, message)).start()
