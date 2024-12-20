import asyncio
from src.bot_instance import bot  # Настроенный бот
from src.app.handlers.handlers import register_handlers
from src.database.db_sessions import reset_database
from src.configs.commands import create_commands


async def start_bot():
    await reset_database()
    await create_commands(bot)
    register_handlers(bot)
    print("Bot is running...")
    await bot.polling()


async def main():
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
