from telethon import TelegramClient, events
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
api_id= os.getenv("API_ID")
api_hash= os.getenv("API_HASH")

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

# Listen for messages in a specific channel
@client.on(events.NewMessage(from_users='Salman'))
async def my_event_handler(event):
    with open('new_messages.txt', 'a') as file:
        file.write(f"{event.text} \n")

# Start the client and keep it running
client.start()
client.run_until_disconnected()