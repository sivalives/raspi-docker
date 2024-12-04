import os
import asyncio
from telethon import TelegramClient

# Initialize the Telegram client
client = TelegramClient(
    os.environ["TELEGRAM_TELETHON_SESSION_NAME"],
    int(os.environ["TELEGRAM_TELETHON_API_ID"]),
    os.environ["TELEGRAM_TELETHON_API_HASH"],
)

async def download_messages_and_files(channel_name: str, download_dir: str = "/tmp", limit: int = None):
    """
    Fetch messages from a specified channel and download attached files.

    Args:
        channel_name (str): Name or ID of the channel to fetch messages from.
        download_dir (str): Directory to save downloaded files. Defaults to '/tmp'.
        limit (int): Maximum number of messages to fetch. Fetches all if None.
    """
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    async with client:
        # Get the channel entity
        channel = await client.get_entity(channel_name)

        # Fetch messages
        messages = await client.get_messages(channel, limit=limit)

        # Process messages
        for message in messages:
            if message.text:
                print(message.text)

            if message.file:
                print(f"Downloading {message.file.name}...")
                file_path = await client.download_media(message, download_dir)
                print(f"File saved to {file_path}")

async def main():
    # Define your channel name here
    channel_name = 'linkedin_learning_Download'

    # Call the function to download messages and files
    await download_messages_and_files(channel_name)

if __name__ == "__main__":
    asyncio.run(main())

