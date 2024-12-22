from telebot import types
from telebot.states.asyncio.context import StateContext
from src.app.states import RegistrateUser
from src.app.text_vars_handlers_ import Translated_Language
from src.app.services.registration import (
    handle_start,
    handle_change_language,
    handle_language_selection,
    handle_name_input,
    handle_last_name_input,
    handle_sex_selection,
    handle_age_input,
    handle_email_input,
    handle_city_input,
    handle_any_state,
    show_rules
)

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    async def start_handler(message: types.Message, state: StateContext):
        await handle_start(bot, message, state)

    @bot.message_handler(commands=['show_rules'])
    async def rules_handler(msg: types.Message):
        await show_rules(bot, msg)

    @bot.message_handler(state="*", commands=["cancel"])
    async def any_state(message: types.Message, state: StateContext):
        await handle_any_state(bot, message, state)

    @bot.message_handler(commands=["lang"])
    async def change_language_handler(message: types.Message):
        await handle_change_language(bot, message)

    @bot.callback_query_handler(func=lambda call: call.data in Translated_Language.langvs,
                                state=RegistrateUser.waiting_for_language)
    async def language_handler(call: types.CallbackQuery, state: StateContext):
        await handle_language_selection(bot, call, state)

    @bot.message_handler(state=RegistrateUser.waiting_for_name)
    async def name_get(message: types.Message, state: StateContext):
        await handle_name_input(bot, message, state)

    @bot.message_handler(state=RegistrateUser.waiting_for_last_name)
    async def last_name_get(message: types.Message, state: StateContext):
        await handle_last_name_input(bot, message, state)

    @bot.callback_query_handler(func=lambda call: call.data in ['male', 'female'],
                                state=RegistrateUser.waiting_for_sex)
    async def sex_handler(call: types.CallbackQuery, state: StateContext):
        await handle_sex_selection(bot, call, state)

    @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=True)
    async def age_get(message: types.Message, state: StateContext):
        await handle_age_input(bot, message, state)

    @bot.message_handler(state=RegistrateUser.waiting_for_email)
    async def email_get(message: types.Message, state: StateContext):
        await handle_email_input(bot, message, state)

    @bot.message_handler(state=RegistrateUser.waiting_for_city)
    async def city_get(message: types.Message, state: StateContext):
        await handle_city_input(bot, message, state)
