from telethon import TelegramClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
api_id= os.getenv("API_ID")
api_hash= os.getenv("API_HASH")

with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))