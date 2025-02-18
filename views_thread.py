import threading
import time
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class ProxyScraper:
    def __init__(self):
        self.proxy_sources = [
            'https://free-proxy-list.net/',
            'https://www.proxynova.com/proxy-server-list',
            'https://www.hide-my-ip.com/proxylist.shtml',
            'https://proxylistplus.com/',
            'https://proxyscrape.com/free-proxy-list'
        ]
        self.proxies_list = []

    def collect_proxies(self):
        threads = []
        for source in self.proxy_sources:
            thread = threading.Thread(target=self.collect_proxies_from_source, args=(source,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return self.proxies_list

    def collect_proxies_from_source(self, source):
        try:
            response = requests.get(source, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    proxy = cols[0].text.strip() + ':' + cols[1].text.strip()
                    self.proxies_list.append(proxy)
        except Exception as e:
            logging.error(f"Error collecting proxies from {source}: {str(e)}")

def send_view(post_url, proxy):
    try:
        proxy_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        user_agents = ['Mozilla/5.0', 'Chrome/103.0.0.0']
        headers = {
            'User-Agent': user_agents[0],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(post_url, headers=headers, proxies=proxy_dict, timeout=60)
        if response.status_code == 200:
            logging.info(f"View sent successfully using proxy {proxy}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending view using proxy {proxy}: {str(e)}")

def start_views_thread(bot, message, post_url):
    try:
        bot.send_message(message.chat.id, "Views thread started!")
        while True:
            proxy_scraper = ProxyScraper()
            proxies_list = proxy_scraper.collect_proxies()
            for proxy in proxies_list:
                threading.Thread(target=send_view, args=(post_url, proxy)).start()
            time.sleep(0.1)  # wait for 0.1 seconds
    except Exception as e:
        bot.send_message(message.chat.id, "Error starting views thread!")
        logging.error(f"Error starting views thread: {str(e)}")
