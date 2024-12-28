from telebot import types
from telebot.states.asyncio.context import StateContext
from src.app.states import RegistrateUser, AgreementRules, LanguageChanger
from src.app.text_vars_handlers_ import Translated_Language as _
from src.app.services.registration import (
    handle_start,
    handle_language_selection,
    handle_name_input,
    handle_last_name_input,
    handle_sex_selection,
    handle_age_input,
    handle_email_input,
    handle_city_input,
    handle_any_state,
)
from src.configs.commands import tcm
from src.app.services.one_reason_handlers.one_reason import (show_rules, handle_rules_acceptance, handle_command_selection,
                                                             handle_callback_data_language)

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    async def start_handler(message: types.Message, state: StateContext):
        await handle_start(bot, message.from_user.id, state)

    @bot.message_handler(commands=['show_rules'])
    async def rules_handler(message: types.Message, state: StateContext):
        await show_rules(bot, message, state)

    @bot.message_handler(state="*", commands=["cancel"])
    async def any_state(message: types.Message, state: StateContext):
        await handle_any_state(bot, message, state)

    @bot.message_handler(commands=["lang"])
    async def change_language_handler(message: types.Message, state: StateContext):
        await handle_command_selection(bot, message, state)

    @bot.message_handler(commands=["cmd_input"])
    async def cmd_input_handler(message: types.Message):
        keyboard = await tcm.commands_inline_keyboard_menu()
        await bot.send_message(message.chat.id, "Choose an option:", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data in ["/start", "/help"])
    #describe menu objects here
    async def parcer(call: types.CallbackQuery, state: StateContext):
        await bot.send_message(call.from_user.id, "activated")
        if call.data == "/start":
            await handle_start(bot, call.from_user.id, state)



    @bot.callback_query_handler(func=lambda call: call.data in _.ACRONYMS,
                                state=LanguageChanger.language)
    async def language_command_handler(call: types.CallbackQuery, state: StateContext):
        await handle_callback_data_language(bot, call, state)


    @bot.callback_query_handler(func=lambda call: call.data in _.ACRONYMS,
                                state=RegistrateUser.waiting_for_language)
    async def language_handler(call: types.CallbackQuery, state: StateContext):
        await handle_language_selection(bot, call, state)

    @bot.message_handler(state=RegistrateUser.waiting_for_start)
    async def name_get(message: types.Message, state: StateContext):
        await handle_start(bot, message, state)

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


    @bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'],
                                state=AgreementRules.waiting_for_agreement)
    async def rules_acceptance_handler(call: types.CallbackQuery, state: StateContext):
        await handle_rules_acceptance(bot, call, state)







    # @bot.message_handler(commands=['accept'])
    # async def accept_handler(message: types.Message):
    #     from src.database.db_sessions import get_param, update_param, get_users
    #     print(message.text)
    #     res = await get_users(message.from_user.id)
    #     if res:
    #         await bot.send_message(message.from_user.id, text="Phase1 OK")
    #         """Phase2"""
    #         res = await get_param(message.from_user.id, param='language')
    #         await bot.send_message(message.from_user.id, text=res)
    #
    #         res = await update_param(message.from_user.id, param='language', value='ES')
    #         await bot.send_message(message.from_user.id, text=res)
    #     else:
    #         await bot.send_message(message.from_user.id, text="Phase1 Failed")

