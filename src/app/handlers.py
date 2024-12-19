from src.database.db_sessions import add_person, get_users
from src.database.models import User
from telebot.asyncio_filters import TextFilter
import logging
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters
from src.middleware.i18n_middleware import keyboards
from src.app.text_vars_handlers_ import users_lang, Translated_Language as TRAN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegistrateUser(StatesGroup):
    waiting_for_name: str = State()
    waiting_for_last_name: str = State()
    waiting_for_sex: str = State()
    waiting_for_age: int = State()
    waiting_for_email: str = State()
    waiting_for_city: str = State()
    waiting_for_language: str = State()


def register_handlers(bot):
    @bot.message_handler(commands="start")
    async def start(message: types.Message, state: StateContext):
        text = TRAN.return_translated_text("start_greeting", id_=message.from_user.id)
        text2 = TRAN.return_translated_text(
            "already_registered", id_=message.from_user.id
        )
        user = await get_users(telegram_id=message.chat.id)

        if user:
            await bot.send_message(message.chat.id, text2)
        else:
            await state.set(RegistrateUser.waiting_for_name)
            await bot.send_message(
                message.chat.id,
                text,
                reply_parameters=ReplyParameters(message_id=message.message_id),
            )

    @bot.message_handler(commands="get_me")
    async def get_me(message: types.Message):
        user = await get_users(message.from_user.id)
        text1 = TRAN.return_translated_text("get_me", id_=message.from_user.id)
        text2 = TRAN.return_translated_text("get_me2", id_=message.from_user.id)
        if user:
            await bot.send_message(message.chat.id, text1)
        else:
            await bot.send_message(
                message.chat.id,
                text2,
            )

    @bot.message_handler(commands=["registration"])
    async def start_ex_(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_name)
        text = TRAN.return_translated_text("start_greeting", id_=message.from_user.id)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Cancel command handler
    @bot.message_handler(state="*", commands=["cancel"])
    async def any_state(message: types.Message, state: StateContext):
        await state.delete()
        text = TRAN.return_translated_text("cancel_command", id_=message.from_user.id)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for first name input
    @bot.message_handler(state=RegistrateUser.waiting_for_name)
    async def name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_last_name)
        text = TRAN.return_translated_text("ask_last_name", id_=message.from_user.id)
        await state.add_data(name=message.text)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for last name input
    @bot.message_handler(state=RegistrateUser.waiting_for_last_name)
    async def last_name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_sex)
        text = TRAN.return_translated_text("ask_sex", id_=message.from_user.id)
        await state.add_data(last_name=message.text)
        await bot.send_message(
            message.chat.id,
            text,
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for sex input
    @bot.message_handler(state=RegistrateUser.waiting_for_sex)
    async def sex_get(message: types.Message, state: StateContext):
        if message.text.lower() in ["male", "female"]:
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

    # Handler for age input
    @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=True)
    async def age_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_email)
        text = TRAN.return_translated_text("ask_email", id_=message.from_user.id)
        await state.add_data(age=message.text)
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

    # Handler for email input
    @bot.message_handler(state=RegistrateUser.waiting_for_email)
    async def email_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_city)
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

        msg = TRAN.format_thank_you_message(message.from_user.id, user_data)


    @bot.message_handler(commands="lang")
    async def change_language_handler(message: types.Message):
        await bot.send_message(
            message.chat.id,
            "Choose language\nВыберите язык\nTilni tanlang",
            reply_markup=keyboards.languages_keyboard(),
        )

    @bot.callback_query_handler(
        func=None, text=TextFilter(contains=["en", "ru", "uz_Latn"])
    )
    async def language_handler(call: types.CallbackQuery):
        lang = call.data
        users_lang[call.from_user.id] = lang
        text = TRAN.return_translated_text("language_changed", id_=0, lang_call=lang)
        # When you changed user language, you have to pass it manually beacause it is not changed in context
        await bot.edit_message_text(text, call.from_user.id, call.message.id)
