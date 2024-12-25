from telebot import TeleBot # Импортируем types
# import yaml
# from src.configs.config import COMMANDS_PATH
from pydantic import BaseModel
from src.bot_instance import bot


class TelebotCommand(BaseModel):
    command: str
    description: str


class TelebotCommandsManager:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.commands = [
            TelebotCommand("/start", "start description"),
            TelebotCommand("/help", "help description"),
            TelebotCommand("/cancel", "cancel description"),
            TelebotCommand("/lang", "lang description"),
        ]

    # async def load_commands(self) -> dict[str, str]:
    #     with open(COMMANDS_PATH, "r", encoding="utf-8") as file:
    #         data = yaml.safe_load(file)
    #         self.commands = [TelebotCommand(**cmd) for cmd in data["commands"]]
    # def command_generator(self):
    #     for command_info in self.commands:
    #         self.commands.append(command_info)
    #         yield types.BotCommand(command_info.command, command_info.description)

    def set_commands(self):
        self.bot.delete_my_commands()  # Убираем await
        self.bot.set_my_commands(commands=[self.commands])  # Убираем await

tcm = TelebotCommandsManager(bot)