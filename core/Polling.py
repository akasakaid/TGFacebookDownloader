import os
import sys
import time
import requests
from .Update import update
from dotenv import load_dotenv

load_dotenv()

tokenbot = os.environ.get("TOKEN_BOT")


def poling():
    offset = 0
    urlUpdate = 'https://api.telegram.org/bot' + tokenbot + '/getUpdates'
    while True:
        try:
            req = requests.get(urlUpdate, params={
                               'offset': offset}, timeout=10)
            data = req.json()
            if len(data['result']) == 0:
                time.sleep(5)
                continue
            offset = data['result'][0]['update_id'] + 1
            update(data['result'][0])
            print("~" * 60)
        except KeyError as e:
            print(req.text)
            continue
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            print("=" * 60)
            continue
        except requests.exceptions.ReadTimeout:
            print("Read Timeout")
            print("=" * 60)
            continue
