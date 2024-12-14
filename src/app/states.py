from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters

class RegistrateUser (StatesGroup):
    waiting_for_name = State()
    waiting_for_last_name = State()
    waiting_for_sex = State()
    waiting_for_age = State()
    waiting_for_email = State()
    waiting_for_city = State()
def register_state_handlers(bot):


    # Start command handler
    @bot.message_handler(commands=["start"])
    async def start_ex(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_name)
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
    @bot.message_handler(state=RegistrateUser .waiting_for_name)
    async def name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_last_name)
        await state.add_data(name=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your last name?",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for last name input
    @bot.message_handler(state=RegistrateUser .waiting_for_last_name)
    async def last_name_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_sex)
        await state.add_data(last_name=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your sex? (male/female)",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for sex input
    @bot.message_handler(state=RegistrateUser .waiting_for_sex)
    async def sex_get(message: types.Message, state: StateContext):
        if message.text.lower() in ['male', 'female']:
            await state.set(RegistrateUser .waiting_for_age)
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
    @bot.message_handler(state=RegistrateUser .waiting_for_age, is_digit=True)
    async def age_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_email)
        await state.add_data(age=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your email?",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for incorrect age input
    @bot.message_handler(state=RegistrateUser .waiting_for_age, is_digit=False)
    async def age_incorrect(message: types.Message):
        await bot.send_message(
            message.chat.id,
            "Please enter a valid number for age.",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for email input
    @bot.message_handler(state=RegistrateUser .waiting_for_email)
    async def email_get(message: types.Message, state: StateContext):
        await state.set(RegistrateUser .waiting_for_city)
        await state.add_data(email=message.text)
        await bot.send_message(
            message.chat.id,
            "What is your city?",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )

    # Handler for city input
    @bot.message_handler(state=RegistrateUser .waiting_for_city)
    async def city_get(message: types.Message, state: StateContext):
        async with state.data() as data:
            # Retrieving all data from state
            name = data.get('name')
            last_name = data.get('last_name')
            sex = data.get('sex')
            age = data.get('age')
            email = data.get('email')
            city = message.text  # city from user input

            msg = (
                f"Thank you for sharing! Here is a summary of your information:\n"
                f"First Name: {name}\n"
                f"Last Name: {last_name}\n"
                f"Sex: {sex}\n"
                f"Age: {age}\n"
                f"Email: {email}\n"
                f"City: {city}"
            )

        await bot.send_message(
            message.chat.id,
            msg,
            parse_mode="html",
            reply_parameters=ReplyParameters(message_id=message.message_id),
        )
        await state.delete()

