from telethon import TelegramClient
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv, find_dotenv
import os
import re
import asyncio
import aiofiles
import pathlib
import json

# loading telegram api
load_dotenv(find_dotenv())
api_id= os.getenv("API_ID")
api_hash= os.getenv("API_HASH")

# reading json for telegram channels url
try:
    with open('channels.json', 'r') as file:
        data = json.load(file)
        channels_url = data["channel"]

except:
    print("failed to read json file")


client = TelegramClient('anon', api_id, api_hash)

async def joinChannel(client, channel):
    try:
        client(JoinChannelRequest(channel))
        print(f'successfully join channel {channel}')
    except:
        print(f'failed to join channel {channel}')

async def scrapeMessage(client, channel, limit):
    idx = 0
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # extracts the name of the telegram channel to use it as folder name
    folder_name = re.split('/', channel)[-1]
    pathlib.Path(folder_name).mkdir(exist_ok=True)
    async for message in client.iter_messages(channel, limit):
        # checks that the message is not empty and is a job post
        if message.text and re.search(email_regex, message.text):
            async with aiofiles.open(f'{folder_name}/job{idx}.txt', mode='w', encoding='utf-8') as f:
                await f.write(message.text)
            idx+=1
async def main():
    for channel in channels_url:
    
        await joinChannel(client, channel=channel)
        await scrapeMessage(client, channel=channel, limit=500)

with client:
    client.loop.run_until_complete(main())
