import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

logging.basicConfig(filename='logs/scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def scrape_channel(client, channel_name):
    try:
        entity = await client.get_entity(channel_name)
        messages = []
        async for message in client.iter_messages(entity, limit=100):  # Limit to 100 for testing; remove for full scrape
            msg_data = {
                'message_id': message.id,
                'channel_name': channel_name,
                'message_date': message.date.isoformat(),
                'message_text': message.text,
                'has_media': message.media is not None,
                'views': message.views,
                'forwards': message.forwards,
                'image_path': None
            }
            if message.photo:
                # Download image
                image_dir = f"data/raw/images/{channel_name}"
                os.makedirs(image_dir, exist_ok=True)
                image_path = f"{image_dir}/{message.id}.jpg"
                await client.download_media(message.photo, image_path)
                msg_data['image_path'] = image_path
                logging.info(f"Downloaded image for message {message.id} in {channel_name}")
            messages.append(msg_data)
        return messages
    except Exception as e:
        logging.error(f"Error scraping {channel_name}: {e}")
        return []
    
async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone)
    channels = ['Chemed', 'lobelia4cosmetics','tikvahpharma']  # Replace with real channel usernames
    all_messages = {}
    for channel in channels:
        msgs = await scrape_channel(client, channel)
        all_messages[channel] = msgs
    
    # Save to data lake as JSON
    today = datetime.now().strftime('%Y-%m-%d')
    os.makedirs(f"data/raw/telegram_messages/{today}", exist_ok=True)
    for channel, msgs in all_messages.items():
        json_path = f"data/raw/telegram_messages/{today}/{channel}.json"
        with open(json_path, 'w') as f:
            json.dump(msgs, f, indent=4)
        logging.info(f"Saved {len(msgs)} messages for {channel} to {json_path}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())