import requests
import telegram
import time
import schedule
import os
import asyncio

from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram bot token and channel ID
bot_token = os.getenv("BOT_ID")
channel_id = os.getenv("CHANNEL_ID")
bot = Bot(token=bot_token)

# News API configuration
news_api_key = os.getenv("NEWSAPI_TOKEN")  # Your News API key
news_url = 'https://newsapi.org/v2/everything'

params = {
    'q': 'cryptocurrency',  # Query for cryptocurrency news
    'apiKey': news_api_key,
    'language': 'en',  # Language of the news
    'sortBy': 'publishedAt',  # Sort by the latest news
    'pageSize': 1  # Number of articles to fetch
}

def fetch_crypto_news():
    response = requests.get(news_url, params=params)
    news_data = response.json()

    if response.status_code == 200 and 'articles' in news_data:
        news_message = "📰 **Latest Crypto News:**\n\n"
        for article in news_data['articles']:
            news_message += (
                f"• **{article['title']}**\n"
                # f"  - {article['description']}\n"
                f"  - ({article['url']})\n\n"
            )
        return news_message
    else:
        return "Failed to fetch crypto news."

async def send_crypto_news():
    news_message = fetch_crypto_news()
    await bot.send_message(chat_id=channel_id, text=news_message, parse_mode=ParseMode.MARKDOWN)

async def schedule_tasks():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

def run_bot():
    # Schedule the bot to run every 5 seconds
    schedule.every(1).hour.do(lambda: asyncio.create_task(send_crypto_news()))

    # Run the scheduler
    asyncio.run(schedule_tasks())

# Run the bot
run_bot()
