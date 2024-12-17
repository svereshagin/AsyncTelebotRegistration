import telebot
import gettext
import os

# Установите путь к каталогу с переводами
locale_path = os.path.join(os.path.dirname(__file__), '../middlewares/'
                                                      'translations')

# Инициализация бота с вашим токеном
API_TOKEN = '7084142136:AAE-P9SMdAWgMzeyl9CpV9Qvd1WVwFp1CVY'
bot = telebot.TeleBot(API_TOKEN)

# Функция для установки языка
def set_language(language_code):
    lang = gettext.translation('messages', localedir=locale_path, languages=[language_code], fallback=True)
    lang.install()
    return lang.gettext

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Устанавливаем язык (например, 'ru' для русского)
    _ = set_language('ru')  # Вы можете динамически определять язык на основе пользователя
    bot.send_message(message.chat.id, _("Hello, World!"))

# Обработчик команды /register
@bot.message_handler(commands=['register'])
def register_command(message):
    _ = set_language('ru')  # Установите язык на нужный
    bot.send_message(message.chat.id, _("User  initiated registration."))

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
