async def handle_incorrect_age(bot, message: types.Message):
    text = TRAN.return_translated_text("age_incorrect", id_=message.from_user.id)
    await bot.send_message(message.chat.id, text)