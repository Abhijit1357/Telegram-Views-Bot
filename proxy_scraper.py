import requests

from bs4 import BeautifulSoup

import time



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

    for source in self.proxy_sources:

      try:

        response = requests.get(source)

        soup = BeautifulSoup(response.text, 'html.parser')

        for row in soup.find_all('tr'):

          cols = row.find_all('td')

          if len(cols) >= 2:

            proxy = cols[0].text.strip() + ':' + cols[1].text.strip()

            self.proxies_list.append(proxy)

      except Exception as e:

        print(f"Error collecting proxies from {source}: {str(e)}")

    return self.proxies_list



  def save_proxies(self, filename):

    with open(filename, 'w') as f:

      for proxy in self.proxies_list:

        f.write(proxy + '
')



Usage

scraper = ProxyScraper()

proxies = scraper.collect_proxies()

scraper.save_proxies('proxies.txt')

print("Proxies collected and saved to proxies.txt")
