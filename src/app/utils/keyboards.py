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
                InlineKeyboardButton(text="Francese", callback_data="fr"),
            ]
        ]
    )


def sex_choose_keyboard(male,female):
    """male and female params are generated in the sex_choose function in module handlers"""
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(male, callback_data="male"),
                InlineKeyboardButton(female, callback_data="female"),
            ]
        ]
    )


def any_agree_keyboard(button1, button2):
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(button1, callback_data="yes"),
                InlineKeyboardButton(button2, callback_data="no"),
            ]
        ]
    )