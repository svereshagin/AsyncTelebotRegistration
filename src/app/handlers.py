from telebot import types
import asyncio
import json
import os
import re
import time
import asyncio

def register_handlers(bot):
    @bot.message_handler(commands="change_my_credentials")
    async def start(message):
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, rules)

    def rules(message):
        if message.from_user.id in [1]: #реализовать получение из бд:
            pass
    #if user_check_db()
    #change_my_info realization
    #создать json file и из него читать и подставлять названия

    # @bot.message_handler(commands=['mainmenu'])
    # async def main_menu(message):
    #     create_inline_keyboard = types.InlineKeyboardMarkup()

    # @bot.message_handler(language_code=['ru'])
    # async def is_russian(message):
    #     bot.reply_to(message, 'You are russian')
    #
    # @bot.message_handler(language_code=['eng'])
    # def is_russian(message):
    #     bot.reply_to(message, 'You are englishman')

