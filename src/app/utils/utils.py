from src.app.utils import keyboards


async def send_language_selection_keyboard(chat_id, bot: object):
    await bot.send_message(
        chat_id,
        "Choose language\nВыберите язык\nPickUp language",
        reply_markup=keyboards.languages_keyboard(),
    )


async def send_sex_selection_keyboard(translated_text, chat_id, bot: object, male, female):
    await bot.send_message(
        chat_id,
        translated_text,
        reply_markup=keyboards.sex_choose_keyboard(male, female)
    )


async def send_rules_agreement_keyboard(text, chat_id, bot: object, button1, button2):
    print(text)
    await bot.send_message(
        chat_id,
        text,
        reply_markup=keyboards.any_agree_keyboard(button1, button2)
    )


    # @bot.message_handler(commands="get_me")
    # async def get_me(message: types.Message):
    #     user = await get_users(message.from_user.id)
    #     text1 = TRAN.return_translated_text("get_me", id_=message.from_user.id)
    #     text2 = TRAN.return_translated_text("get_me2", id_=message.from_user.id)
    #     if user:
    #         await bot.send_message(message.chat.id, text1)
    #     else:
    #         await bot.send_message(
    #             message.chat.id,
    #             text2,
    #         )

    # @bot.message_handler(commands=["registration"])
    # async def start_ex_(message: types.Message, state: StateContext):
    #     await state.set(RegistrateUser.waiting_for_name)
    #     text = TRAN.return_translated_text("start_greeting", id_=message.from_user.id)
    #     await bot.send_message(
    #         message.chat.id,
    #         text,
    #         reply_parameters=ReplyParameters(message_id=message.message_id),
    #     )


    # Handler for first name input

    # Handler for last name input


    # Handler for sex input

    # Handler for age input
    # @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=True)
    # async def age_get(message: types.Message, state: StateContext):
    #     await state.set(RegistrateUser.waiting_for_email)
    #     text = TRAN.return_translated_text("ask_email", id_=message.from_user.id)
    #     await state.add_data(age=message.text)
    #     await bot.send_message(
    #         message.chat.id,
    #         text,
    #         reply_parameters=ReplyParameters(message_id=message.message_id),
    #     )
    #
    # # Handler for incorrect age input
    # @bot.message_handler(state=RegistrateUser.waiting_for_age, is_digit=False)
    # async def age_incorrect(message: types.Message):
    #     text = TRAN.return_translated_text("age_incorrect", id_=message.from_user.id)
    #     await bot.send_message(
    #         message.chat.id,
    #         text,
    #         reply_parameters=ReplyParameters(message_id=message.message_id),
    #     )
    #
    # # Handler for email input
    # @bot.message_handler(state=RegistrateUser.waiting_for_email)
    # async def email_get(message: types.Message, state: StateContext):
    #     await state.set(RegistrateUser.waiting_for_city)
    #     text = TRAN.return_translated_text("ask_city", id_=message.from_user.id)
    #     await state.add_data(email=message.text)
    #     await bot.send_message(
    #         message.chat.id,
    #         text,
    #         reply_parameters=ReplyParameters(message_id=message.message_id),
    #     )
    #
    # @bot.message_handler(state=RegistrateUser.waiting_for_city)
    # async def city_get(message: types.Message, state: StateContext):
    #     user_data = {}
    #     async with state.data() as data:
    #         user_data = {'first_name': data.get("name"),
    #                 'last_name': data.get("last_name"),
    #                 'sex': 1 if data.get("sex") == "male" else 0,
    #                 'age': int(data.get("age")),
    #                 'email': data.get("email"),
    #                 'city': message.text,
    #                 }
    #         user = User(
    #             first_name=user_data["first_name"],
    #             last_name=user_data["last_name"],
    #             sex=user_data['sex'],
    #             age=user_data['age'],
    #             telegram_id=message.from_user.id,
    #             email=user_data["email"],
    #             city=user_data['city']
    #         )
    #     msg = TRAN.format_thank_you_message(message.from_user.id , user_data)
    #
    #     await add_person(user)
    #     await bot.send_message(
    #         message.chat.id,
    #         msg,
    #         parse_mode="html",
    #         reply_parameters=ReplyParameters(message_id=message.message_id),
    #     )
    #     await state.delete()
    #
    # @bot.message_handler(commands="choose_sex_keyboard")
    # async def choose_sex_keyboard(message: types.Message):
    #     to_user = TRAN.return_translated_text("choose_sex", message.from_user.id)
    #     male_button = TRAN.return_translated_text("male", message.from_user.id)
    #     female_button = TRAN.return_translated_text("female", message.from_user.id)
    #     await bot.send_message(
    #         message.chat.id,
    #         text=to_user,
    #         reply_markup=keyboards.sex_choose_keyboard(male=male_button, female=female_button),
    #     )
    #
    # @bot.callback_query_handler(func=lambda call: True, state=RegistrateUser.waiting_for_language)
    # async def language_handler(call: types.CallbackQuery, state: StateContext):
    #     lang = call.data
    #     users_lang[call.from_user.id] = lang
    #     text = TRAN.return_translated_text("language_changed", id_=0, lang_call=lang)
    #
    #     await bot.edit_message_text(text, call.from_user.id, call.message.id)
    # async def continue_handler_after_language(message)
    #     # После выбора языка, переходим к следующему состоянию
    #     await state.set(RegistrateUser.waiting_for_name)
    #     text_welcome = TRAN.return_translated_text("start_greeting", id_=call.from_user.id)
    #     await bot.send_message(call.from_user.id, text_welcome)

