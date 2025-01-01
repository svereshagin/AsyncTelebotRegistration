import asyncio
from src.bot_instance import bot
from src.app.handlers.handlers import register_handlers
from src.database.db_sessions import reset_database
from src.configs.commands import tcm
from src.configs.keyboard_manager import initialize_keyboard_manager


async def start_bot():
    await reset_database()
    await tcm.set_start_commands()
    register_handlers(bot)
    print("Bot is running...")
    await bot.polling()


async def main():
    await initialize_keyboard_manager()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())