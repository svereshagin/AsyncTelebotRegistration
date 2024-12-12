import asyncio
from src.database.db_sessions import add_person
from src.database.models import User
import logging
from telebot.asyncio_handler_backends import ContinueHandling
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    @bot.message_handler(commands="techies")
    async def techies_command(message):
        await bot.send_message(message.chat.id, "Do u like techies?")
        bot.register_next_step_handler(message, process_techies_response)

    async def process_techies_response(message):
        if message.text.lower() == 'yes':
            await bot.send_message(message.chat.id, "FUCK U")
        else:
            await bot.send_message(message.chat.id, "I too bruda")

    @bot.message_handler(commands=['start'])
    async def start(message):
        await bot.send_message(message.chat.id, 'Hello World!')
        return ContinueHandling()


    @bot.message_handler(commands=['start'])
    async def start2(message):
        """
        This handler comes after the first one, but it will never be called.
        But you can call it by returning ContinueHandling() in the first handler.

        If you return ContinueHandling() in the first handler, the next
        registered handler with appropriate filters will be called.
        """
        await bot.send_message(message.chat.id, 'Hello World2!')