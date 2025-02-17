import requests
import time
from config import Config
from proxies import ProxyScraper
import threading


def increase_views():
  proxy_scraper = ProxyScraper()
  proxies_list = proxy_scraper.collect_proxies()


  views_sent = 0
  max_views = Config.MAX_VIEWS_PER_INTERVAL


  while views_sent < max_views:
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


        url = f'https://t.me/{Config.CHANNEL_USERNAME}/{Config.POST_ID}'
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)


        if response.status_code == 200:
          views_sent += 1
          print(f'Views sent: {views_sent}')
        else:
          print(f'Proxy {proxy} blocked or invalid')


      except Exception as e:
        print(f'Error with proxy {proxy}: {str(e)}')


      if views_sent >= max_views:
        break

    time.sleep(Config.VIEWS_SENDING_INTERVAL)


  print('Views sending limit reached or completed')
