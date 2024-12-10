from telebot.async_telebot import AsyncTeleBot
from src.app.handlers import register_handlers
from .config import TOKEN
import asyncio
from src.database.database import engine
# from sqlalchemy.orm import Session
#
# session = Session()
bot = AsyncTeleBot(TOKEN, protect_content='True')


def main():
    register_handlers(bot)
    asyncio.run(bot.polling())

if __name__ == '__main__':
    main()
    engine.connect()
