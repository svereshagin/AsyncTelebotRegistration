import os

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
from src.configs.config import COMMANDS_PATH
load_dotenv()

class InlineKeyboardManager:
    """class for inline keyboard manager
       takes args from file and formates
       then buttons"""
    def __init__(self):
        self.menu = []

    def get_commands(self):
        pass

    def load_buttons(self, key):
        """Loads buttons from .yaml file and makes a list of commands out of it"""
        with open("commands.yaml", "r") as file:
            data = yaml.safe_load(file)
            menu_items = data['inline_keyboard']['menu']

            if isinstance(menu_items, list):
                self.menu = menu_items  # Просто копируем список
            else:
                raise ValueError(f"Unexpected type for 'menu': {type(menu_items)}")

            print(self.menu)

IKM = InlineKeyboardManager()
IKM.load_buttons(COMMANDS_PATH)