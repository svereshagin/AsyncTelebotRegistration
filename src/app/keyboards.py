from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def languages_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(text="English", callback_data="en"),
                InlineKeyboardButton(text="Русский", callback_data="ru"),
                InlineKeyboardButton(text="Italiano", callback_data="it"),
            ]
        ]
    )

def sex_choose_keyboard(male: str ,female: str):
    """male and female params are generated in the sex_choose function in module handlers"""
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(male, callback_data="male"),
                InlineKeyboardButton(female, callback_data="female"),
            ]
        ]
    )
