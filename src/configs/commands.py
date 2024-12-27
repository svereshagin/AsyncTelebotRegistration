from email import message_from_bytes
from src.app.text_vars_handlers_ import _
from telebot import TeleBot, types
from pydantic import BaseModel
from src.bot_instance import bot


class TelebotCommand(BaseModel):
    command: str
    description: str


class TelebotCommandsManager:
    """Class provides more elegant and structured working with commands"""
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.commands = [
            TelebotCommand(command="/start", description="start description"),
            TelebotCommand(command="/help", description="help description"),
            TelebotCommand(command="/cancel", description="cancel description"),
            TelebotCommand(command="/lang", description="lang description"),
            TelebotCommand(command="/show_rules", description="lang description"),
            TelebotCommand(command="/my_settings", description="my_settings description"),
        ]



    async def set_start_commands(self):
        await bot.delete_my_commands(scope=None, language_code=None)
        commands = [types.BotCommand(cmd.command, cmd.description) for cmd in self.commands]
        await bot.set_my_commands(commands=commands)


    async def commands_inline_keyboard_menu(self, user_id):
        """Send inline keyboard menu for user"""
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        # Create buttons for each command
        buttons = [
            types.InlineKeyboardButton(text=_(cmd.command, id_= user_id), callback_data=cmd.command) for cmd in self.commands
        ]

        # Add buttons to the keyboard
        keyboard.add(*buttons)

        return keyboard

tcm = TelebotCommandsManager(bot)