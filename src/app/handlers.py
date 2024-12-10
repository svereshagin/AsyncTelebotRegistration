import asyncio
from ..database.db_sessions import get_db_session
from ..database.models import *

def register_handlers(bot):
    @bot.message_handler(commands="change_my_credentials")
    async def start(message):
        await bot.send_message(message.chat.id, f'{message.__dict__}')  # Отправляем текст сообщения
        await bot.send_message(message.chat.id, f'{message.from_user.first_name}')
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, "Пожалуйста, введите ваши новые данные:")
        bot.register_next_step_handler(message, rules)  # Переходим к следующему шагу

    def rules(message):
        bot.reply_to(message, f'Вы ввели: {message.text}')  # Отправляем ответ с текстом сообщения

        # Здесь можете добавить логику для обработки новых данных пользователя
        # Например, сохранение в базу данных

    def registration(msg):
        user(msg.from_user.first_name, msg.from_user.last_name, msg.from_user)
        # Здесь вы можете реализовать логику регистрации пользователя

# Пример использования
# register_handlers(bot)
