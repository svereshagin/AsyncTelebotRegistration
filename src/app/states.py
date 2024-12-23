from telebot.states import State, StatesGroup


class RegistrateUser(StatesGroup):
    waiting_for_name: State = State()
    waiting_for_last_name: State = State()
    waiting_for_sex: State = State()
    waiting_for_age: State = State()
    waiting_for_email: State = State()
    waiting_for_city: State = State()
    waiting_for_language: State = State()


class AgreementRules(StatesGroup):
    waiting_for_agreement: State = State()

class LanguageChanger(StatesGroup):
    language: State = State()