from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_filters import TextMatchFilter, StateFilter, IsDigitFilter
from telebot.states.asyncio.middleware import StateMiddleware
from src.configs.config import settings
from src.middleware.i18n_middleware.my_translator import (
    I18NMiddleware,
)  # Если используете i18n
from src.configs.config import TRANSLATIONS_PATH

# Создаём state storage
state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
i18n = I18NMiddleware(translations_path=TRANSLATIONS_PATH, domain_name="messages")

bot = AsyncTeleBot(settings.TOKEN, protect_content=True, state_storage=state_storage)
# Настройка i18n middleware (если используется)
bot.setup_middleware(i18n)
# Добавляем middleware для состояния
bot.setup_middleware(StateMiddleware(bot))
# Добавляем кастомные фильтры
bot.add_custom_filter(TextMatchFilter())
bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(IsDigitFilter())

# Экспортируем бот и i18n (если нужно)
__all__ = ["bot", "i18n"]
