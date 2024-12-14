def inline_keyboard(bot):
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    def create_inline_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Button 1", callback_data="button1")
        button2 = types.InlineKeyboardButton("Button 2", callback_data="button2")
        keyboard.add(button1, button2)  # Add buttons to the keyboard
        return keyboard

    @dp.message_handler(commands=["start"])
    async def send_welcome(message: types.Message):
        await message.answer(
            "Welcome! Choose an option:", reply_markup=create_inline_keyboard()
        )

    @dp.callback_query_handler(lambda call: True)
    async def handle_query(call: types.CallbackQuery):
        if call.data == "button1":
            await call.answer("You pressed Button 1!")
            await call.message.answer("You selected Button 1.")
        elif call.data == "button2":
            await call.answer("You pressed Button 2!")
            await call.message.answer("You selected Button 2.")
