import os
from telethon import TelegramClient, events, sync
from dotenv import load_dotenv

load_dotenv()

apiid = os.environ.get("API_ID")
apihash = os.environ.get("API_HASH")
tokenbot = os.environ.get("TOKEN_BOT")


def sendMessage(chat_id: int, message: str, message_id: int):
    try:
        if not os.path.exists("session"):
            os.makedirs("session")
        app = TelegramClient(session=f"session/bot",
                             api_id=apiid, api_hash=apihash)
        app.start(bot_token=tokenbot)
        app.send_message(entity=chat_id, message=message, reply_to=message_id)
        app.disconnect()
    except Exception as e:
        app.disconnect()
        print(f"- {e}")
