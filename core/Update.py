
import os
import requests
from datetime import datetime
from module.messageText import *
from lib.sendVideo import sendVideo
from lib.sendMessage import sendMessage
from lib.facebookDownloader import FacebookDownloader


def update(data):
    if 'callback_query' in str(data):
        data = data['callback_query']
        msgid = data['message']['message_id']
        userid = data['message']['chat']['id']
        firstname = data['message']['chat']['first_name']
        text = data['data']
        dateFormat = datetime.fromtimestamp(data["message"]["date"])
    else:
        msgid = data['message']['message_id']
        userid = data['message']['chat']['id']
        firstname = data['message']['chat']['first_name']
        text = data['message']['text']
        dateFormat = datetime.fromtimestamp(data["message"]["date"])
    startText = startTextFunction(firstname=firstname)
    print(
        f'- {dateFormat} - {userid} - {firstname} - {text}')
    requests.post('https://api.akasakaid.dev/api/addusertiktok',
                  data={'userid': userid, 'first_name': firstname})
    if 'm.facebook.com' in text:
        text = text.replace('m.facebook.com', 'www.facebook.com')
    if text.startswith('/start'):
        sendMessage(chat_id=userid, message=startText, message_id=msgid)
        return
    if text.startswith('/donation'):
        sendMessage(chat_id=userid, message=donationText, message_id=msgid)
        return
    if text.startswith('/about'):
        sendMessage(chat_id=userid, message=aboutText, message_id=msgid)
        return
    if text.startswith('http') and 'facebook.com' in text or text.startswith('http') and 'fb.watch' in text:
        dl = FacebookDownloader()
        first = dl.alpha_version(url=text)
        # print(first)
        if first is not None:
            output_name, note = first
            sendVideo(chat_id=userid, video=output_name, message_id=msgid)
            try:
                os.remove(output_name)
            except PermissionError:
                pass
            return
        else:
            beta = dl.beta_version(url=text)
            # print(beta)
            if beta is not None:
                output_name, note = beta
                sendVideo(chat_id=userid, video=output_name, message_id=msgid)
                try:
                    os.remove(output_name)
                except PermissionError:
                    pass
                return
            else:
                sendMessage(chat_id=userid, message=failedText,
                            message_id=msgid)
                return
