from src.database.db_sessions import add_person, get_users
from src.database.models import User
import logging
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters
import gettext
from src.app import keyboards

_ = ""

gettext.bindtextdomain("messages", "locales")
gettext.textdomain("messages")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegistrateUser (StatesGroup):
    waiting_for_language: str = State()
    waiting_for_name: str = State()
    waiting_for_last_name: str = State()
    waiting_for_sex: str = State()
    waiting_for_age: int = State()
    waiting_for_email = State()
    waiting_for_city = State()





def register_handlers(bot):
    def send_message(chat_id, text, message_id=None):
        """Упрощенная функция для отправки сообщений."""
        return bot.send_message(chat_id, text, reply_parameters=ReplyParameters(message_id=message_id))
    @bot.message_handler(commands="start")
    async def start(message: types.Message, state: StateContext):
        user = await get_users(telegram_id=message.chat.id)
        if user:
            await send_message(message.chat.id, _("You are already registered."))
        else:
            logger.info(f"User  {message.from_user.id} initiated registration.")
            await state.set(RegistrateUser .waiting_for_language)
            await send_message(message.chat.id, _("Choose your language:"), reply_markup=keyboards.languages_keyboard())

    @bot.callback_query_handler(func=lambda call: call.data in ['en', 'ru', 'uz_Latn'], state=RegistrateUser .waiting_for_language)
    async def language_selected(call: types.CallbackQuery, state: StateContext):
        global _
        language = call.data
        lang = gettext.translation("messages", localedir="locales", fallback=True, languages=[language])
        lang.install()
        _ = lang.gettext

        await state.add_data(language=language)
        await send_message(call.message.chat.id, _("Hello! What is your first name?"))
        await state.set(RegistrateUser .waiting_for_name)

    @bot.message_handler(state=RegistrateUser .waiting_for_name)
    async def name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_last_name)
        await state.add_data(name=message.text)
        await send_message(message.chat.id, _("What is your last name?"))

    @bot.message_handler(state=RegistrateUser .waiting_for_last_name)
    async def last_name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_sex)
        await state.add_data(last_name=message.text)
        await send_message(message.chat.id, _("What is your sex? (male/female)"))

    @bot.message_handler(state=RegistrateUser .waiting_for_sex)
    async def sex_get(message: types.Message, state: StateContext):
        if message.text.lower() in ['male', 'female']:
            await state.set(RegistrateUser .waiting_for_age)
            await state.add_data(sex=message.text)
            await send_message(message.chat.id, _("What is your age?"))
        else:
            await send_message(message.chat.id, _("Please enter 'male' or 'female'."))

    @bot.message_handler(state=RegistrateUser .waiting_for_age, is_digit=True)
    async def age_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_email)
        await state.add_data(age=message.text)
        await send_message(message.chat.id, _("What is your email?"))

    @bot.message_handler(state=RegistrateUser .waiting_for_email)
    async def email_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_city)
        await state.add_data(email=message.text)
        await send_message(message.chat.id, _("What is your city?"))

    @bot.message_handler(state=RegistrateUser .waiting_for_city)
    async def city_get(message: types.Message, state: StateContext):
        async with state.data() as data:
            user = User(
                first_name=data.get('name'),
                last_name=data.get('last_name'),
                sex=1 if data.get("sex") == "male" else 0,
                age=int(data.get('age')),
                telegram_id=message.from_user.id,
                email=data.get('email'),
                city=message.text
            )

            msg = (
                f"Thank you for sharing! Here is a summary of your information:\n"
                f"First Name: {data.get('name')}\n"
                f"Last Name: {data.get('last_name')}\n"
                f"Sex: {'male' if data.get('sex') == 'male' else 'female'}\n"
                f"Age: {data.get('age')}\n"
                f"Email: {data.get('email')}\n"
                f"City: {message.text}\n"
                f"Language: {data.get('language')}"
            )

        await add_person(user)
        await send_message(message.chat.id, msg)
        await state.delete()

    @bot.message_handler(state="*", commands=["cancel"])
    async def cancel_command(message: types.Message, state: StateContext):
        await state.delete()
        await send_message(message.chat.id, _("Your information has been cleared. Type /start to begin again."))

    @bot.message_handler(commands="get_me")
    async def get_me(message: types.Message):
        user = await get_users(message.from_user.id)
        if user:
            await send_message(message.chat.id, _("Your account already exists."))
        else:
            await send_message(message.chat.id, _("You do not have an account. Proceed with registration by /add_me."))

    @bot.message_handler(commands=["registration"])
    async def start_ex_(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_name)
        await send_message(message.chat.id, _("Hello! What is your first name?\nYou can skip the process with /cancel command."))

    @bot.message_handler(commands='lang')
    async def change_language_handler(message: types.Message):
        await send_message(message.chat.id, _("Choose language\nВыберите язык\nTilni tanlang"), reply_markup=keyboards.languages_keyboard())