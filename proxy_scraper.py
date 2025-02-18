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

    def check_proxy_speed(self, proxy):
        try:
            response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=10)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def check_proxy_uptime(self, proxy):
        try:
            response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=10)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def check_proxy_anonymity(self, proxy):
        try:
            response = requests.get("https://www.whatismyip.com/", proxies={"http": proxy, "https": proxy}, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            ip_address = soup.find("span", {"class": "ip"}).text.strip()
            if ip_address != requests.get("https://api.ipify.org").text.strip():
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def get_high_quality_proxies(self):
        high_quality_proxies = []
        for proxy in self.proxies_list:
            if self.check_proxy_speed(proxy) and self.check_proxy_uptime(proxy) and self.check_proxy_anonymity(proxy):
                high_quality_proxies.append(proxy)
        return high_quality_proxies

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
            high_quality_proxies = self.get_high_quality_proxies()
            self.save_proxies('high_quality_proxies.txt')
            logging.info("High quality proxies collected and saved to high_quality_proxies.txt")
            time.sleep(0.1)  # wait for 0.1 seconds

if __name__ == '__main__':
    ProxyScraper().main()
