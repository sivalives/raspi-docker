import os
import asyncio
from telethon import TelegramClient
from telethon.tl import functions, types

client = TelegramClient(os.environ["TELEGRAM_TELETHON_SESSION_NAME"], os.environ["TELEGRAM_TELETHON_API_ID"], os.environ["TELEGRAM_TELETHON_API_HASH"])
client.start()

async def main():
    channel = await client.get_entity('iptvxtream1')
    messages = await client.get_messages(channel, limit= None) #pass your own args

    #then if you want to get all the messages text
    for x in messages:
        print(x.text) #return message.text


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
