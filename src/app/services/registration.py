import logging
import re
from telebot import types, TeleBot
from telebot.states.asyncio.context import StateContext
from src.app.utils.utils import ( send_sex_selection_keyboard)
from src.app.states import RegistrateUser
from src.database.db_sessions import add_person, get_users
from src.database.models import User
from src.app.text_vars_handlers_ import Translated_Language as _
from telebot.types import ReplyParameters

from src.configs.commands import tcm


logger = logging.getLogger(__name__)
user_data = {}


async def handle_start(bot, user_id, state: StateContext):
    """
    Handles the /start command. Checks if the user is registered, and if not, initiates the registration process.
    If the user is already registered, then we proceed with the main part of the programm and show menu
    Args:
        bot: Telegram bot instance.
        user_id: Alternative to message.from_user.id because of TG restrictions of bot2bot.
        state: Context of the current state.

    Returns:
        None
    """
    is_registered = await get_users(user_id)

    if is_registered == 1:
        text = _.translate('REG',"greetings.already_registered", user_id = user_id)
        await bot.send_message(user_id, text)
        await tcm.commands_inline_keyboard_menu()
        return

    text = _.translate('REG',"greetings.start", user_id = user_id)
    await bot.send_message(user_id, text=text)
    await state.set(RegistrateUser.waiting_for_language)
    text = _.translate("REG", "prompts.ask_language", user_id = user_id)
    await bot.send_message(
                user_id,
                text,
                reply_markup= _.languages_keyboard())

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
    _.users_lang[call.from_user.id] = lang
    text = _.translate('REG', "greetings.language_changed", user_id = call.from_user.id)
    await bot.edit_message_text(text, call.from_user.id, call.message.id)
    await state.add_data(language=lang)
    text = _.translate('REG',"prompts.ask_name", user_id=call.from_user.id)
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
    text = _.translate('REG', "prompts.ask_last_name", user_id=message.from_user.id)
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
        male = _.translate('REG', "responses.male", user_id=message.from_user.id)
        female = _.translate('REG',"responses.female", user_id=message.from_user.id)
        translated_text = _.translate("BUTT","choose_sex", user_id=message.from_user.id)
        await send_sex_selection_keyboard(translated_text, message.chat.id, bot, male, female)
    except Exception as e:
        logger.error(f"Error sending sex selection keyboard: {e}")
        text = _.translate("REG", "erorrs.Error", user_id=message.from_user.id)
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
    text = _.translate("REG", "responses.data_received", user_id=call.from_user.id)
    await bot.send_message(call.message.chat.id, text)

    await state.set(RegistrateUser.waiting_for_age)
    text = _.translate("REG","prompts.ask_age", user_id=call.from_user.id)
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
    pattern = r'^\d+$'

    if re.match(pattern, message.text):
        age = int(message.text)
        if age < 0 or age > 120:
            await handle_incorrect_age(bot, message)
            return

        await state.set(RegistrateUser.waiting_for_email)
        await state.add_data(age=age)
        text = _.translate("REG", "responses.data_received", user_id=message.from_user.id)
        await bot.send_message(message.chat.id, text)
        text = _.translate("REG","prompts.ask_email", user_id=message.from_user.id)
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
    text = _.translate("REG", "prompts.age_incorrect", user_id=message.from_user.id)
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
    text = _.translate("REG", "responses.data_received", user_id=message.from_user.id)
    await bot.send_message(message.chat.id, text)
    text = _.translate("REG", "prompts.ask_city", user_id=message.from_user.id)
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
    # user_data = {}
    # Извлекаем данные из состояния
    async with state.data() as data:
        try:
            # user_data = {
            #     'language': data.get("language"),
            #     'first_name': data.get("name"),
            #     'last_name': data.get("last_name"),
            #     'sex': 1 if data.get("sex") == "male" else 0,
            #     'age': int(data.get("age")),
            #     'email': data.get("email"),
            #     'city': message.text,
            # }

            user = User(
                language=data.get("language", "en"),
                first_name=data.get("name"),
                last_name=data.get("last_name"),
                sex=1 if data.get("sex") == "male" else 0,
                age=int(data.get("age")),
                telegram_id=message.from_user.id,
                email=data.get("email"),
                city=message.text,
            )
        except (TypeError, ValueError) as e:
            # Отправляем сообщение об ошибке, если данные некорректны
            await bot.send_message(message.chat.id, _.translate("REG", "errors.Error", user_id = message.from_user.id))
            return

    msg = _.translate("REG", "user_data", user_id=message.from_user.id)
    msg = msg.format(
        name=user.first_name, last_name=user.last_name,
        sex=user.sex, age=user.age,
        email=user.email, city=user.city,
        language=user.language
    )
    await add_person(user)
    await bot.send_message(
        message.chat.id,
        msg,
        parse_mode="html",
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    await state.delete()



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
    # text = TRAN.return_translated_text("cancel_command", id_=message.from_user.id)
    text = ""
    await bot.send_message(message.chat.id, text)
