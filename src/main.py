import telebot
from src.config.config import TOKEN
from src.app.handlers import register_handlers

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, message.text)

def main():
    # register_handlers(bot)
    bot.infinity_polling()

if __name__ == '__main__':
    main()