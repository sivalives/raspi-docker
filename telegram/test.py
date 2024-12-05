import os
import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument

# Set your credentials (or use environment variables for security)
API_ID = int(os.getenv("TELEGRAM_TELETHON_API_ID"))
API_HASH = os.getenv("TELEGRAM_TELETHON_API_HASH")
SESSION_NAME = os.getenv("TELEGRAM_TELETHON_SESSION_NAME")

# Initialize the Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def download_files_this_week(contact_username, download_path="./downloads"):
    # Ensure the download directory exists
    os.makedirs(download_path, exist_ok=True)

    # Start the Telegram client
    await client.start()

    # Get the contact entity
    contact = await client.get_entity(contact_username)

    # Fetch messages (increase limit if needed)
    messages = await client.get_messages(contact, limit=100)

    # Get the start of the current week in UTC
    now = datetime.now(timezone.utc)
    start_of_week = now - timedelta(days=now.weekday())

    for message in messages:
        # Ensure the date is timezone-aware
        if message.date >= start_of_week:
            # Print message details
            print(f"Message ID {message.id}: {message.text or 'No text content'}")

            # Check for media in the primary message
            if message.file and isinstance(message.media, MessageMediaDocument):
                file_name = message.file.name or f"file_{message.id}"
                print(f"Downloading file: {file_name}")

                # Download the file
                file_path = await client.download_media(message, file=download_path)
                print(f"File saved to {file_path}")
            # Check for media in forwarded messages
            elif message.forward and message.forward.original_fwd:
                forwarded_media = message.forward.original_fwd
                if forwarded_media.file and isinstance(forwarded_media.media, MessageMediaDocument):
                    file_name = forwarded_media.file.name or f"file_{message.id}_forwarded"
                    print(f"Downloading forwarded file: {file_name}")

                    # Download the file
                    file_path = await client.download_media(forwarded_media, file=download_path)
                    print(f"Forwarded file saved to {file_path}")
                else:
                    print(f"Forwarded message ID {message.id} does not contain a file.")
            else:
                print(f"Message ID {message.id} does not contain a file.")
        else:
            print(f"Message ID {message.id} is older than this week. Skipping.")

# Run the async function
asyncio.run(download_files_this_week("Deepika"))

