from telebot.async_telebot import AsyncTeleBot
from src.app.handlers import register_handlers
from src.database.db_sessions import reset_database
from src.config import settings
import asyncio


bot = AsyncTeleBot(settings.TOKEN, protect_content=True)


async def start_bot():
    await reset_database()
    register_handlers(bot)
    print("ok")
    await bot.polling()


async def main():
    await start_bot()


if __name__ == '__main__':
    asyncio.run(main())

