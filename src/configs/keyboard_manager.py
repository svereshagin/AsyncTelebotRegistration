from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import yaml
from src.app.translator import Translated_Language as _
from src.bot_instance import bot


class InlineKeyboardManager:
    """Класс для управления инлайн-кнопками,
       загружает кнопки из файла и формирует их."""

    def __init__(self):
        self.menu = None  # Изначально меню равно None
        self.session = None
    async def initialize(self):
        """Асинхронная инициализация меню"""
        self.menu = await self.load_buttons('menu')
        self.session = await self.load_buttons('session')

    async def load_buttons(self, key):
        try:
            with open("src/configs/commands.yaml", "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                print("Loaded data:", data)
                menu_items = data.get('inline_keyboard', {}).get(key, {})
                if isinstance(menu_items, dict):
                    return menu_items
                else:
                    raise ValueError(f"Unexpected type for 'menu': {type(menu_items)}")
        except FileNotFoundError:
            print("Error: File 'commands.yaml' not found.")
            raise
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            raise
        except Exception as e:
            print(f"Error loading buttons: {e}")
            raise

    def get_menu(self):
        if self.menu is None:
            raise ValueError("Menu is not loaded properly.")

        buttons = [
            [InlineKeyboardButton(text=command, callback_data=data)]
            for command, data in self.menu.items()
        ]
        return InlineKeyboardMarkup(buttons)

    def get_session(self):
        if self.session is None:
            raise ValueError("Session is not loaded properly.")

        buttons = [
            [InlineKeyboardButton(text=command, callback_data=data)]
            for command, data in self.session.items()
        ]
        return InlineKeyboardMarkup(buttons)

    def sex_choose_keyboard(self, user_id):
        """male and female params are generated in the sex_choose function in module handlers"""
        button1 = _.translate('REG', "responses.male", user_id=user_id)
        button2 = _.translate('REG',"responses.female", user_id=user_id)
        return InlineKeyboardMarkup(
            keyboard=[
                [
                    InlineKeyboardButton(button1, callback_data="male"),
                    InlineKeyboardButton(button2, callback_data="female"),
                ]
            ]
        )

    def any_agree_keyboard(self, user_id):
        button1 = _.translate('BUTT', "yes", user_id)
        button2 = _.translate('BUTT',"no", user_id)
        return InlineKeyboardMarkup(
            keyboard=[
                [
                    InlineKeyboardButton(button1, callback_data="yes"),
                    InlineKeyboardButton(button2, callback_data="no"),
                ]
            ]
        )

    async def send_sex_selection_keyboard(self, user_id):
        translated_text = _.translate("BUTT","choose_sex", user_id=user_id)
        await bot.send_message(
            user_id,
            translated_text,
            reply_markup=self.sex_choose_keyboard(user_id)
        )

    async def send_rules_agreement_keyboard(self, user_id):
        text = _.translate("BUTT", "choose_sex", user_id)
        await bot.send_message(
            user_id,
            text,
            reply_markup=self.any_agree_keyboard(user_id)
        )


IKM = InlineKeyboardManager()


async def initialize_keyboard_manager():
    await IKM.initialize()
