import asyncio
from typing import Union
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from src.middleware.i18n_middleware.i18n_base_middleware import I18N
from telebot.asyncio_storage.memory_storage import StateMemoryStorage


class I18NMiddleware(I18N):

    def process_update_types(self) -> list:
        """
        Here you need to return a list of update types which you want to be processed
        """
        return ["message", "callback_query"]

    async def get_user_language(self, obj: Union[types.Message, types.CallbackQuery]):
        """
        This method is called when new update comes (only updates which you return in 'process_update_types' method)
        Returned language will be used in 'pre_process' method of parent class
        Returned language will be set to context language variable.
        If you need to get translation with user's actual language you don't have to pass it manually
        It will be automatically passed from context language value.
        However if you need some other language you can always pass it.
        """

        user_id = obj.from_user.id

        if user_id not in users_lang:
            users_lang[user_id] = "en"

        return users_lang[user_id]


users_lang = {}
