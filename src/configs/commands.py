import telebot
import yaml
import os
from src.configs.config import COMMANDS_PATH

async def load_commands():
    with open(COMMANDS_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def command_generator(data):
    for command_info in data["commands"]:
        yield telebot.types.BotCommand(
            command_info["command"], command_info["description"]
        )


async def create_commands(bot):
    commands = await load_commands()
    print("Загруженные команды:", commands)  # Для отладки
    await bot.delete_my_commands(scope=None, language_code=None)
    await bot.set_my_commands(commands=command_generator(commands))
