import requests
from bs4 import BeautifulSoup
import logging
import threading
import json
import time
import concurrent.futures

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
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.collect_proxies_from_source, self.proxy_sources)
        self.proxies_list = list(set(self.proxies_list))  # remove duplicates
        self.proxies_list = [proxy for proxy in self.proxies_list if self.validate_proxy(proxy)]  # validate proxies
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

    def validate_proxy(self, proxy):
        try:
            requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
            return True
        except requests.exceptions.RequestException:
            return False

    def update_proxy_sources(self):
        # new proxy sources add karne ke liye code yahaan aayega
        pass

    def save_proxies(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(self.proxies_list, f)
        except Exception as e:
            logging.error(f"Error saving proxies to {filename}: {str(e)}")

    def load_proxies(self, filename):
        try:
            with open(filename, 'r') as f:
                self.proxies_list = json.load(f)
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
