import asyncio
from src.database.db_sessions import add_person, get_users
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
        logger.info(f"Received command 'add_me' from {message.from_user.first_name} {message.from_user.last_name}.")
        await asyncio.sleep(1)
        user = User(first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    telegram_id=message.from_user.id)
        await add_person(user)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "You have been added!")  # Example response

    @bot.message_handler(commands="get_me")
    async def start(message):
        user = await get_users(message.from_user.id)
        if user:
            await bot.send_message(message.chat.id, "Your acc Is already exists")
        else:
            await bot.send_message(message.chat.id, "You do not have acc, proceed with registration by /add_me")


    # Initialize the bot

    # Define states
    class MyStates(StatesGroup):
        techies_response = State()

    # Start command handler
    @bot.message_handler(commands=["start"])
    async def start(msg):
        pass


