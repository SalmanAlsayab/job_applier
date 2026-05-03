from telethon import TelegramClient
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from dotenv import load_dotenv, find_dotenv
import os
import re
import asyncio
import aiofiles
import win32com.client as win32

# olApp = win32.Dispatch('Outlook.Application')
# olNS = olApp.GetNameSpace('MAPI')


load_dotenv(find_dotenv())
api_id= os.getenv("API_ID")
api_hash= os.getenv("API_HASH")

client = TelegramClient('anon', api_id, api_hash)

async def joinChannel(client, channel):
    try:
        client(JoinChannelRequest(channel))
        print(f'successfully join channel {channel}')
    except:
        print(f'failed to join channel {channel}')

async def scrapeMessage(client, channel, limit):
    idx = 0
    async for message in client.iter_messages(channel, limit):
        if message.text:
            async with aiofiles.open(f'jobs/job{idx}.txt', mode='w', encoding='utf-8') as f:
                await f.write(message.text)
            idx+=1
async def main():
   await joinChannel(client, channel='https://t.me/itcjobs')
   await scrapeMessage(client, channel='https://t.me/itcjobs', limit=1)

with client:
    client.loop.run_until_complete(main())
