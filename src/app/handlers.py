from src.database.db_sessions import add_person, get_users
from src.database.models import User
from telebot.asyncio_filters import TextFilter
import logging
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters
from src.middleware.i18n_middleware_example.my_translator import _, __
from src.middleware.i18n_middleware_example import keyboards
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users_lang = {}


class RegistrateUser (StatesGroup):
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
        lang = users_lang.get(message.from_user.id, 'en')
        text = _("Hello ! What is your first name?\n You can skip the process with /cancel command.", lang=lang)
        user = await get_users(telegram_id=message.chat.id)

        if user:
            await bot.send_message(message.chat.id, _("You are already registered", lang=users_lang.get(message.from_user.id, 'en')))
        else:
            await state.set(RegistrateUser.waiting_for_name)
            text = _("Hello ! What is your first name?\n You can skip the process with /cancel command.",lang=users_lang.get(message.from_user.id, 'en'))
            await bot.send_message(
                message.chat.id, text,
                reply_parameters=ReplyParameters(message_id=message.message_id),
            )

    @bot.message_handler(commands="get_me")
    async def get_me(message: types.Message):
        user = await get_users(message.from_user.id)
        if user:
            await bot.send_message(message.chat.id, "Your account already exists.")
        else:
            await bot.send_message(
                message.chat.id,
                "You do not have an account. Proceed with registration by /add_me.",
            )

    @bot.message_handler(commands=["registration"])
    async def start_ex_(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_name)
        await bot.send_message(
            message.chat.id,
            "Hello! What is your first name?\n"
            "You can skip the process with /cancel command.",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Cancel command handler
    @bot.message_handler(state="*", commands=["cancel"])
    async def any_state(message: types.Message, state: StateContext):
        await state.delete()
        await bot.send_message(
            message.chat.id,
            "Your information has been cleared. Type /start to begin again.",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for first name input
    @bot.message_handler(state=RegistrateUser.waiting_for_name)
    async def name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_last_name)
        await state.add_data(name=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your last name?",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for last name input
    @bot.message_handler(state=RegistrateUser.waiting_for_last_name)
    async def last_name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_sex)
        await state.add_data(last_name=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your sex? (male/female)",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for sex input
    @bot.message_handler(state=RegistrateUser.waiting_for_sex)
    async def sex_get(message: types.Message, state: StateContext):
        if message.text.lower() in ['male', 'female']:
            await state.set(RegistrateUser.waiting_for_age)
            await state.add_data(sex=message.text)
            await bot.send_message(
                message.chat.id,
                "What is your age?",
                reply_parameters=ReplyParameters(message_id=message.message_id),
            )
        else:
            await bot.send_message(
                message.chat.id,
                "Please enter 'male' or 'female'.",
                reply_parameters=ReplyParameters(message_id=message.message_id),
            )

    # Handler for age input
    @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=True)
    async def age_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_email)
        await state.add_data(age=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your email?",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for incorrect age input
    @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=False)
    async def age_incorrect(message: types.Message):
        await bot.send_message(
            message.chat.id,
            "Please enter a valid number for age.",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for email input
    @bot.message_handler(state=RegistrateUser.waiting_for_email)
    async def email_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser.waiting_for_city)
        await state.add_data(email=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your city?",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for city input
    # Handler for city input
    @bot.message_handler(state=RegistrateUser.waiting_for_city)
    async def city_get(message: types.Message, state: StateContext):
        async with state.data() as data:
            # Retrieve information from state data
            first_name = data.get('name')
            last_name = data.get('last_name')
            sex = 1 if data.get("sex") == "male" else 0
            age = int(data.get('age'))
            email = data.get('email')
            city = message.text  # city from user input
            # Create User instance
            user = User(
                first_name=first_name,
                last_name=last_name,
                sex=sex,
                age=age,
                telegram_id=message.from_user.id,
                email=email,
                city=city
            )

            msg = (
                f"Thank you for sharing! Here is a summary of your information:\n"
                f"First Name: {first_name}\n"
                f"Last Name: {last_name}\n"
                f"Sex: {'male' if sex == 1 else 'female'}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"City: {city}"
            )

        await add_person(user)
        await bot.send_message(
            message.chat.id,
            msg,
            parse_mode="html",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )
        await state.delete()








    @bot.message_handler(commands='lang')
    async def change_language_handler(message: types.Message):
        await bot.send_message(message.chat.id, "Choose language\nВыберите язык\nTilni tanlang",
                               reply_markup=keyboards.languages_keyboard())


    @bot.callback_query_handler(func=None, text=TextFilter(contains=['en', 'ru', 'uz_Latn']))
    async def language_handler(call: types.CallbackQuery):
        lang = call.data
        users_lang[call.from_user.id] = lang

        # When you changed user language, you have to pass it manually beacause it is not changed in context
        await bot.edit_message_text(_("Language has been changed", lang=lang), call.from_user.id, call.message.id)

    @bot.message_handler(commands='menu')
    async def menu_handler(message: types.Message):
        text = _("This is ReplyKeyboardMarkup menu example in multilanguage bot.")
        await bot.send_message(message.chat.id, text, reply_markup=keyboards.menu_keyboard(_))




















