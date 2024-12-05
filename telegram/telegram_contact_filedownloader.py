import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument

# Set your credentials (or use environment variables for security)
API_ID = os.getenv("TELEGRAM_TELETHON_API_ID")
API_HASH = os.getenv("TELEGRAM_TELETHON_API_HASH")
SESSION_NAME = os.getenv("TELEGRAM_TELETHON_SESSION_NAME")

# Initialize the Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def download_file_from_contact(contact_username, download_path="./downloads"):
    # Ensure the download directory exists
    os.makedirs(download_path, exist_ok=True)

    # Connect to Telegram
    await client.start()

    # Get the contact entity
    contact = await client.get_entity(contact_username)

    # Fetch the most recent messages from the contact
    messages = await client.get_messages(contact, limit=20)

    for message in messages:
        # Check if the message contains a file
        if message.file and isinstance(message.media, MessageMediaDocument):
            file_name = message.file.name or f"file_{message.id}"
            print(f"Downloading file: {file_name}")
            
            # Download the file
            file_path = await client.download_media(message, file=download_path)
            print(f"File saved to {file_path}")
        else:
            print(f"Message ID {message.id} does not contain a file.")

# Run the async function
asyncio.run(download_file_from_contact("contact_username_here"))

