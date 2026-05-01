from telethon import TelegramClient
from telethon import TelegramClient, events
from dotenv import load_dotenv, find_dotenv
import os
import re
import win32com.client as win32

olApp = win32.Dispatch('Outlook.Application')
olNS = olApp.GetNameSpace('MAPI')


load_dotenv(find_dotenv())
api_id= os.getenv("API_ID")
api_hash= os.getenv("API_HASH")

client = TelegramClient('anon', api_id, api_hash)

@client.on(events.NewMessage(from_users='IT Jobs وظائف تَقنيّة'))
async def my_event_handler(event):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = re.findall(email_regex, event.raw_text)
    if email:
        mailItem = olApp.CreateItem(0)
        mailItem.Subject = 'Hello 123'
        mailItem.BodyFormat = 1
        mailItem.Body = 'Hello There'
        mailItem.To = 'alzlmsiyab@outlook.com'
        mailItem.Sensitivity  = 2
        mailItem._oleobj_.Invoke(*(64209, 0, 8, 0, olNS.Accounts.Item('SalmanSiy2002@outlook.com')))

async def main():
    pass

with client:
    client.loop.run_until_complete(main())