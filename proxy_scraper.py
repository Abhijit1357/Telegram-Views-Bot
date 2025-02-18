import requests
from bs4 import BeautifulSoup
import logging
import threading
import pickle
import time

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
                    if ':' in proxy and len(proxy.split(':')) == 2:
                        self.proxies_list.append(proxy)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error collecting proxies from {source}: {str(e)}")

    def save_proxies(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.proxies_list, f)
        except Exception as e:
            logging.error(f"Error saving proxies to {filename}: {str(e)}")

    def load_proxies(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.proxies_list = pickle.load(f)
        except Exception as e:
            logging.error(f"Error loading proxies from {filename}: {str(e)}")

    def main(self):
        while True:
            self.proxies_list = []
            self.collect_proxies()
            self.save_proxies('proxies.txt')
            logging.info("Proxies collected and saved to proxies.txt")
            time.sleep(0.1)  # wait for 0.1 seconds

if __name__ == '__main__':
    ProxyScraper().main()
