import os

class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7729465278:AAF_Ao-SfzIleZiiENbkx32uv7UPCTGOXc4')
    TELEGRAM_API_ID = int(os.environ.get('TELEGRAM_API_ID', '22834593'))
    TELEGRAM_API_HASH = os.environ.get('TELEGRAM_API_HASH', 'f400bc1d1baeb9ae93014ce3ee5ea835')
    CHANNEL_USERNAME = os.environ.get('CHANNEL_USERNAME', '@Abt_Abhi')
    POST_ID = os.environ.get('POST_ID', '-1002485988122')
    PROXY_LIST_FILE = os.environ.get('PROXY_LIST_FILE', 'proxies.txt')
    MAX_VIEWS_PER_INTERVAL = int(os.environ.get('MAX_VIEWS_PER_INTERVAL', '1000000'))
    VIEWS_SENDING_INTERVAL = int(os.environ.get('VIEWS_SENDING_INTERVAL', '3600'))
    THREADS_COUNT = int(os.environ.get('THREADS_COUNT', '500'))
    LOGGER_ID = int(os.environ.get('LOGGER_ID', '-1002134425165'))
