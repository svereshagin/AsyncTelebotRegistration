from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
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