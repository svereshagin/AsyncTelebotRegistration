from telebot.async_telebot import AsyncTeleBot
from src.app.handlers import register_handlers
from src.database.db_sessions import reset_database
from src.config import settings
import asyncio
from src.configs.commands import create_commands
from telebot import asyncio_filters
from telebot.asyncio_filters import TextMatchFilter
from telebot.asyncio_storage import StateMemoryStorage
from telebot.states.asyncio.middleware import StateMiddleware
from src.middleware.i18n_middleware_example.my_translator import i18n

state_storage = StateMemoryStorage()  # don't use this in production; switch to redis

bot = AsyncTeleBot(settings.TOKEN, protect_content=True, state_storage=state_storage)
# Add custom filters
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(asyncio_filters.IsDigitFilter())
bot.add_custom_filter(asyncio_filters.TextMatchFilter())

# necessary for state parameter in handlers.

bot.setup_middleware(StateMiddleware(bot))

# Start polling


async def start_bot():
    bot.setup_middleware(i18n)
    bot.add_custom_filter(TextMatchFilter())
    await reset_database()
    await create_commands(bot)
    register_handlers(bot)
    print("ok")
    await bot.polling()


async def main():
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
