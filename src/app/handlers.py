from src.database.db_sessions import add_person, get_users
from src.database.models import User
import logging
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters
from src.app.text_vars_handlers_ import users_lang, ControllText as CTRLTEXT, Translated_Language as TRAN, \
    Translated_Language
from src.app.utils import send_language_selection_keyboard as langv_keyboard, \
    send_sex_selection_keyboard as sex_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegistrateUser(StatesGroup):
    waiting_for_name: State = State()
    waiting_for_last_name: State = State()
    waiting_for_sex: State = State()
    waiting_for_age: State = State()
    waiting_for_email: State = State()
    waiting_for_city: State = State()
    waiting_for_language: State = State()


def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    async def start_handler(message: types.Message, state: StateContext):
        is_registered = await get_users(message.from_user.id)

        if is_registered == 1:
            text = TRAN.return_translated_text("already_registered", id_=message.from_user.id)
            await bot.send_message(message.from_user.id, text)
            return

        text = TRAN.return_translated_text("start", id_ = message.from_user.id)
        await bot.send_message(message.from_user.id, text=text)
        await state.set(RegistrateUser.waiting_for_language)  # Устанавливаем состояние ожидания языка

        await langv_keyboard(message.chat.id, bot)
        await bot.delete_message(message.chat.id, message.message_id)


    @bot.message_handler(commands=["lang"])
    async def change_language_handler(message: types.Message):
        await langv_keyboard(message.chat.id, bot)



    @bot.callback_query_handler(func=lambda call: call.data in Translated_Language.langvs,
                                state=RegistrateUser.waiting_for_language)
    async def language_handler(call: types.CallbackQuery, state: StateContext):
        a = get_users(call.message.from_user.id)
        print(a)
        #bot.send_message(call.message.from_user.id, "You are already registered.")
        lang = call.data
        users_lang[call.from_user.id] = lang
        text = TRAN.return_translated_text("language_changed", id_=0, lang_call=lang)

        # Изменяем текст сообщения о смене языка
        await bot.edit_message_text(text, call.from_user.id, call.message.id)
        text = TRAN.return_translated_text("ask_name", id_=0, lang_call=lang)
        # Переходим к следующему состоянию
        await state.set(RegistrateUser.waiting_for_name)  # Переход к следующему состоянию
        await bot.send_message(call.from_user.id, text=text)  # Запрос имени

    # Handler for first name input
    @bot.message_handler(state=RegistrateUser.waiting_for_name)
    async def name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_last_name)
        text = TRAN.return_translated_text("ask_last_name", id_=message.from_user.id)
        await state.add_data(name=message.text)
        await bot.send_message(
            message.from_user.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    @bot.message_handler(state=RegistrateUser.waiting_for_last_name)
    async def last_name_get(message: types.Message, state: StateContext):
        await state.add_data(last_name=message.text)
        text = TRAN.return_translated_text("data_received", id_=message.from_user.id)
        text = TRAN.return_translated_text("ask_sex", id_=message.from_user.id)
        await state.set(RegistrateUser.waiting_for_sex)

        try:
            male = TRAN.return_translated_text("male", id_=message.from_user.id)
            female = TRAN.return_translated_text("female", id_=message.from_user.id)
            translated_text = TRAN.return_translated_text("Choose_sex", id_=message.from_user.id)
            await sex_keyboard(translated_text, message.chat.id, bot, male, female)
        except Exception as e:
            logger.error(f"Error sending sex selection keyboard: {e}")
            await bot.send_message(message.from_user.id, "An error occurred while trying to send the keyboard.")

    @bot.callback_query_handler(func=lambda call: call.data in ['male', 'female'],
                                state=RegistrateUser.waiting_for_sex)
    async def sex_handler(call: types.CallbackQuery, state: StateContext):
        text = TRAN.return_translated_text("data_received", id_=call.from_user.id)
        await bot.send_message(call.message.chat.id, text)

        await state.set(RegistrateUser.waiting_for_age)  # Переход к следующему состоянию
        await bot.send_message(call.from_user.id, "Please enter your age.")  # Запрос возраста

    @bot.message_handler(state=RegistrateUser.waiting_for_sex)
    async def get_sex(message: types.Message, state: StateContext):
        if message.text.lower() in CTRLTEXT.control_sex:
            await state.set(RegistrateUser.waiting_for_age)
            text = TRAN.return_translated_text("ask_age", id_=message.from_user.id)
            await state.add_data(sex=message.text)
            await bot.send_message(
                message.chat.id,
                text,
                reply_parameters=ReplyParameters(message_id=message.message_id),
            )
        else:
            text = TRAN.return_translated_text("sex_get_response_error", id_=message.from_user.id)
            await bot.send_message(
                message.chat.id,
                text,
                reply_parameters=ReplyParameters(message_id=message.message_id),
            )

    @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=True)
    async def age_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_email)
        await state.add_data(age=message.text)
        text = TRAN.return_translated_text("data_received", id_=message.from_user.id)
        bot.send_message(message.chat.id, text)
        text = TRAN.return_translated_text("ask_email", id_=message.from_user.id)
        await bot.send_message(message.chat.id, text)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for incorrect age input
    @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=False)
    async def age_incorrect(message: types.Message):
        text = TRAN.return_translated_text("age_incorrect", id_=message.from_user.id)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    @bot.message_handler(state=RegistrateUser.waiting_for_email)
    async def email_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_city)
        text = TRAN.return_translated_text("data_received", id_=message.from_user.id)
        bot.send_message(message.chat.id, text)
        text = TRAN.return_translated_text("ask_city", id_=message.from_user.id)
        await state.add_data(email=message.text)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    @bot.message_handler(state=RegistrateUser.waiting_for_city)
    async def city_get(message: types.Message, state: StateContext):
        user_data = {}
        text = TRAN.return_translated_text("data_received", id_=message.from_user.id)
        bot.send_message(message.chat.id, text)
        async with state.data() as data:
            user_data = {'first_name': data.get("name"),
                    'last_name': data.get("last_name"),
                    'sex': 1 if data.get("sex") == "male" else 0,
                    'age': int(data.get("age")),
                    'email': data.get("email"),
                    'city': message.text,
                    }
            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                sex=user_data['sex'],
                age=user_data['age'],
                telegram_id=message.from_user.id,
                email=user_data["email"],
                city=user_data['city']
            )
        msg = TRAN.format_thank_you_message(message.from_user.id , user_data)

        await add_person(user)
        await bot.send_message(
            message.chat.id,
            msg,
            parse_mode="html",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )
        await state.delete()


    @bot.message_handler(state="*", commands=["cancel"])
    async def any_state(message: types.Message, state: StateContext):
        await state.delete()
        text = TRAN.return_translated_text("cancel_command", id_=message.from_user.id)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )