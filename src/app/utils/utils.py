from src.app.utils import keyboards
from telebot import async_telebot


async def send_sex_selection_keyboard(translated_text, chat_id, bot: async_telebot, male, female):
    await bot.send_message(
        chat_id,
        translated_text,
        reply_markup=keyboards.sex_choose_keyboard(male, female)
    )


async def send_rules_agreement_keyboard(text, chat_id, bot: async_telebot, button1, button2):
    print(text)
    await bot.send_message(
        chat_id,
        text,
        reply_markup=keyboards.any_agree_keyboard(button1, button2)
    )
