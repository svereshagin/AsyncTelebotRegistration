import asyncio
from src.database.db_sessions import add_person
from src.database.models import User
import logging
from telebot.asyncio_handler_backends import ContinueHandling

from telebot import async_telebot, asyncio_filters, types
from telebot.asyncio_storage import StateMemoryStorage
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

state_storage = StateMemoryStorage()  # Don't use this in production; switch to redis


def register_handlers(bot):
    @bot.message_handler(commands="add_me")
    async def start(message):
        logger.info(
            f"Received command 'add_me' from {message.from_user.first_name} {message.from_user.last_name}."
        )
        await asyncio.sleep(1)
        user = User(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            telegram_id=message.from_user.id,
        )
        await add_person(user)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(
            message.chat.id, "You have been added!"
        )  # Example response

    # Initialize the bot

    # Define states
    class MyStates(StatesGroup):
        techies_response = State()

    # Start command handler
    @bot.message_handler(commands=["start"])
    async def start_ex(message: types.Message, state: StateContext):
        await bot.send_message(
            message.chat.id,
            "Hello! Type /techies to start a conversation about techies.",
        )

    # Techies command handler
    @bot.message_handler(commands=["techies"])
    async def techies_command(message: types.Message, state: StateContext):
        await state.set(MyStates.techies_response)
        await bot.send_message(message.chat.id, "Do you like techies? (Yes/No)")

    # Handler for techies response
    @bot.message_handler(state=MyStates.techies_response)
    async def process_techies_response(message: types.Message, state: StateContext):
        if message.text.lower() == "yes":
            await bot.send_message(message.chat.id, "FUCK U")
        elif message.text.lower() == "no":
            await bot.send_message(message.chat.id, "I too bruda")
        else:
            await bot.send_message(message.chat.id, "Please answer with 'Yes' or 'No'.")
            return  # Не удаляем состояние, чтобы пользователь мог повторить ответ

        # Удаляем состояние после обработки
        await state.delete()

    # Cancel command handler /cancel
    @bot.message_handler(state="*", commands=["cancel"])
    async def cancel_command(message: types.Message, state: StateContext):
        await state.delete()
        await bot.send_message(
            message.chat.id,
            "Your information has been cleared. Type /start to begin again.",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Add custom filters
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))

    # Necessary for state parameter in handlers.
    from telebot.states.asyncio.middleware import StateMiddleware

    bot.setup_middleware(StateMiddleware(bot))
