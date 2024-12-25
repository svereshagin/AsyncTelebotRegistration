import logging
import re
from telebot import types, TeleBot
from telebot.states.asyncio.context import StateContext
from src.app.utils.utils import (send_language_selection_keyboard, send_sex_selection_keyboard)
from src.app.states import RegistrateUser
from src.database.db_sessions import add_person, get_users
from src.database.models import User
from src.app.text_vars_handlers_ import users_lang, Translated_Language as TRAN, _
from telebot.types import ReplyParameters










logger = logging.getLogger(__name__)
user_data = {}
async def handle_start(bot, message: types.Message, state: StateContext):
    """
    Handles the /start command. Checks if the user is registered, and if not, initiates the registration process.
    If the user is already registered, then we proceed with the main part of the programm and show menu
    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    is_registered = await get_users(message.from_user.id)

    if is_registered == 1:
        #make main part
        text = _("already_registered", id_=message.from_user.id)
        await bot.send_message(message.from_user.id, text)
        return

    text = _("start", id_=message.from_user.id)
    await bot.send_message(message.from_user.id, text=text)
    await state.set(RegistrateUser.waiting_for_language)
    await send_language_selection_keyboard(message.chat.id, bot)
    await bot.delete_message(message.chat.id, message.message_id)


async def handle_language_selection(bot, call: types.CallbackQuery, state: StateContext, flag=False):
    """
    Handles the language selection callback and updates the user's preferred language.

    Args:
        bot: Telegram bot instance.
        call: Callback query object.
        flag: additional for lang_command
        state: Context of the current state.

    Returns:
        None
    """
    if flag:
        return
    lang = call.data
    users_lang[call.from_user.id] = lang
    text = _("language_changed", id_=0, lang_call=lang)
    await bot.edit_message_text(text, call.from_user.id, call.message.id)
    await state.add_data(language=lang)
    text = _("ask_name", id_=0, lang_call=lang)
    await state.set(RegistrateUser.waiting_for_name)
    await bot.send_message(call.from_user.id, text=text)


async def handle_name_input(bot, message: types.Message, state: StateContext):
    """
    Handles the user's input for their first name and prompts for their last name.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    await state.set(RegistrateUser.waiting_for_last_name)
    text = _("ask_last_name", id_=message.from_user.id)
    await state.add_data(name=message.text)
    await bot.send_message(message.from_user.id, text)


async def handle_last_name_input(bot, message: types.Message, state: StateContext):
    """
    Handles the user's input for their last name and prompts for their sex.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    await state.add_data(last_name=message.text)
    await state.set(RegistrateUser.waiting_for_sex)
    try:
        male = _("male", id_=message.from_user.id)
        female = _("female", id_=message.from_user.id)
        translated_text = _("Choose_sex", id_=message.from_user.id)
        await send_sex_selection_keyboard(translated_text, message.chat.id, bot, male, female)
    except Exception as e:
        logger.error(f"Error sending sex selection keyboard: {e}")
        await bot.send_message(message.from_user.id, "An error occurred while trying to send the keyboard.")


async def handle_sex_selection(bot, call: types.CallbackQuery, state: StateContext):
    """
    Handles the user's selection of their sex and prompts for their age.

    Args:
        bot: Telegram bot instance.
        call: Callback query object.
        state: Context of the current state.

    Returns:
        None
    """
    text = _("data_received", id_=call.from_user.id)
    await bot.send_message(call.message.chat.id, text)

    await state.set(RegistrateUser.waiting_for_age)
    text = _("ask_age", id_=call.from_user.id)
    await bot.send_message(call.from_user.id, text)


async def handle_age_input(bot, message: types.Message, state: StateContext):
    """
    Handles the user's input for their age and validates it.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    pattern = r'^[0-9]{1,2}$'

    if re.match(pattern, message.text):
        age = int(message.text)
        if age < 0 or age > 120:
            await handle_incorrect_age(bot, message)
            return

        await state.set(RegistrateUser.waiting_for_email)
        await state.add_data(age=age)
        text = _("data_received", id_=message.from_user.id)
        await bot.send_message(message.chat.id, text)
        text = _("ask_email", id_=message.from_user.id)
        await bot.send_message(message.chat.id, text)
    else:
        await handle_incorrect_age(bot, message)


async def handle_incorrect_age(bot, message: types.Message):
    """
    Notifies the user if their age input is incorrect.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.

    Returns:
        None
    """
    text = _("age_incorrect", id_=message.from_user.id)
    await bot.send_message(message.chat.id, text)


async def handle_email_input(bot, message: types.Message, state: StateContext):
    """
    Handles the user's input for their email and prompts for their city.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    await state.set(RegistrateUser.waiting_for_city)
    text = _("data_received", id_=message.from_user.id)
    await bot.send_message(message.chat.id, text)
    text = _("ask_city", id_=message.from_user.id)
    await state.add_data(email=message.text)
    await bot.send_message(message.chat.id, text)


async def handle_city_input(bot, message: types.Message, state: StateContext):
    """
    Handles the user's input for their city and finalizes the registration process.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    text = _("data_received", id_=message.from_user.id)
    await bot.send_message(message.chat.id, text)
    async with state.data() as data:
        user = User(
            language = data.get("language"),
            first_name = data.get("name"),
            last_name = data.get("last_name"),
            sex = 1 if data.get("sex") == "male" else 0,
            age = int(data.get("age")),
            telegram_id=message.from_user.id,
            email = data.get("email"),
            city = message.text
        )
    await bot.send_message(message.chat.id, "reg_done")
    text = _(user.__repr__(), message.from_user.id)
    print(text)
    await add_person(user)
    await state.delete()
    await bot.send_message(
        message.chat.id,
        text = text,
        parse_mode="html",
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )


async def handle_any_state(bot, message: types.Message, state: StateContext):
    """
    Handles cancellation of any state.

    Args:
        bot: Telegram bot instance.
        message: Incoming message object.
        state: Context of the current state.

    Returns:
        None
    """
    await state.delete()
    text = TRAN.return_translated_text("cancel_command", id_=message.from_user.id)
    await bot.send_message(message.chat.id, text)
