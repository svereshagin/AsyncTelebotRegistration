from telebot.async_telebot import AsyncTeleBot
from src.app.handlers import register_handlers
from .config import settings
import asyncio
# from src.database.models import async_main
bot = AsyncTeleBot(settings.TOKEN, protect_content=True)


def main():
    register_handlers(bot)
    asyncio.run(bot.polling())

if __name__ == '__main__':
    # asyncio.run(async_main())
    main()

