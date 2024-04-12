from aiogram import Bot
import os
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')


# Create a Bot instance using the provided token with HTML parsing mode
bot = Bot(TOKEN, parse_mode='HTML')