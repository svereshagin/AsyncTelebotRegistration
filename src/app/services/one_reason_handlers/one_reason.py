from src.app.translator import Translated_Language as _
from telebot.states.asyncio.context import StateContext
from src.app.states import LanguageChanger, AgreementRules
from telebot import types
from src.configs.keyboard_manager import IKM




async def show_rules(bot , message: types.Message, state: StateContext) -> None:
    """
    Sends the rules to the user and displays agreement options.

    Args:
        bot (types.Bot): Telegram bot instance.
        message (types.Message): Incoming message object.
        state (StateContext): Context of the current state.

    Returns:
        None
    """
    await bot.delete_message(message.chat.id, message.message_id)
    text = _.translate("show_rules", user_id=message.from_user.id)
    print(text)
    await bot.send_message(message.chat.id, text)
    await IKM.send_rules_agreement_keyboard(message.chat.id,)

    await state.set(AgreementRules.waiting_for_agreement)


async def handle_rules_acceptance(bot, call: types.CallbackQuery, state: StateContext) -> None:
    """
    Handles the user's response to the rules agreement.

    Args:
        bot (types.Bot): Telegram bot instance.
        call (types.CallbackQuery): Callback query object.
        state (StateContext): Context of the current state.

    Returns:
        None
    """
    print("Обработчик принятия правил сработал")
    if call.data == 'yes':
        await bot.send_message(call.from_user.id, "Вы приняли правила!")
        # Add logic to record agreement in the database
    else:
        await bot.send_message(call.from_user.id, "Вы отклонили правила.")
        await state.delete()


async def handle_command_selection(bot, message: types.Message, state: StateContext) -> None:
    """
    Initiates the language selection process.

    Args:
        bot (types.Bot): Telegram bot instance.
        message (types.Message): Incoming message object.
        state (StateContext): Context of the current state.

    Returns:
        None
    """
    await state.set(LanguageChanger.language)
    await bot.send_message(
        message.from_user.id,
        text = _.translate("REG", "prompts.ask_language", user_id = message.from_user.id),
        reply_markup=_.languages_keyboard())
    await bot.delete_message(message.chat.id, message.message_id)


async def handle_callback_data_language(bot, call: types.CallbackQuery, state: StateContext) -> None:
    """
    Processes the language selection callback and updates the user's preferred language.

    Args:
        bot (types.Bot): Telegram bot instance.
        call (types.CallbackQuery): Callback query object.
        state (StateContext): Context of the current state.

    Returns:
        None
    """
    lang = call.data
    _.users_lang[call.from_user.id] = lang
    text = _.translate("REG","greetings.language_changed", user_id=call.from_user.id)
    await bot.edit_message_text(text, call.from_user.id, call.message.id)
    await state.delete()
