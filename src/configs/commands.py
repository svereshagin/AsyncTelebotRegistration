from telebot import TeleBot, types  # Импортируем types
from pydantic import BaseModel
from src.bot_instance import bot


class TelebotCommand(BaseModel):
    command: str
    description: str


class TelebotCommandsManager:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.commands = [
            TelebotCommand(command="/start", description="start description"),
            TelebotCommand(command="/help", description="help description"),
            TelebotCommand(command="/cancel", description="cancel description"),
            TelebotCommand(command="/lang", description="lang description"),
        ]

    async def set_start_commands(self):
        await bot.delete_my_commands(scope=None, language_code=None)
        commands = [types.BotCommand(cmd.command, cmd.description) for cmd in self.commands]
        await bot.set_my_commands(commands=commands)



tcm = TelebotCommandsManager(bot)