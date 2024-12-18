from telebot.states import State, StatesGroup


class RegistrateUser(StatesGroup):
    waiting_for_name = State()
    waiting_for_last_name = State()
    waiting_for_sex = State()
    waiting_for_age = State()
    waiting_for_email = State()
    waiting_for_city = State()
