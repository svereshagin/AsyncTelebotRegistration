from typing import Optional

from src.bot_instance import i18n

users_lang = {}

class Translated_Language:
    # Словарь для хранения информации о языке пользователя
    langvs = ["fr", 'ru', 'it', 'en']
    # Словарь с переводами
    TRANSLATED = {
        #start
        "start": "Hello! Proceed with the registration\nYou can skip the process with /cancel command.\n"
                 "Also you can return to registration with\n /registration or /start commands", #also for registration
        "already_registered": "You are already registered.",
        "ask_name": "What is your name?",
        "Choose_sex": "Choose_sex",
        "data_received": "data_received",
        #get_me handler
        "get_me": "You do not have an account. Proceed with registration by /add_me.",
        "get_me2": "Your account already exists.",
        #cancel_handler
        "cancel_command": "Your information has been cleared. Type /start to begin again.",
        #state_handlers
        "ask_last_name": "What is your last name?",
        "ask_sex": "What is your sex? (male/female)",
        "sex_get_response_error": "Please enter 'male' or 'female'.",
        "ask_age": "What is your age?",
        "ask_email": "What is your email?",
        "ask_city": "What is your city?",
        "header": "Thank you for sharing! Here is a summary of your information:\n",
        "first_name": "First Name: {first_name}\n",
        "last_name": "Last Name: {last_name}\n",
        "sex": "Sex: {sex}\n",
        "age": "Age: {age}\n",
        "email": "Email: {email}\n",
        "city": "City: {city}",
        "age_incorrect": "Please enter a valid number for age.",
        "language_changed": "Language has been changed",
        "male": "male",
        "female": "female",
        "any_yes_button": "yes",
        "any_no_button": "no",
        "show_rules_question": "rules",
        "show_rules": "rules",
    }

    @staticmethod
    def return_translated_text(text_key: str, id_: Optional[int], lang_call=0) -> str:
        """Метод для возврата переведенного текста на основе ключа.
        :param text_key: текст отправленный для создания
        :param id_ : id пользователя для нахождения пользователя в словаре
        :param lang_call: oprional, just in case of callback_query situation
        """
        if text_key == "thank_you":
            return i18n.gettext(
                Translated_Language.TRANSLATED.get('header', ""), lang=lang_call
            )
        if lang_call:
            print(lang_call, "ok")
            return i18n.gettext(
                Translated_Language.TRANSLATED.get(text_key, ""), lang=lang_call
            )
        return i18n.gettext(
            Translated_Language.TRANSLATED.get(text_key, ""),
            lang=users_lang.get(id_, "en"),
        )

    @staticmethod
    def format_thank_you_message(user_id_msg, data: dict):
        # Формируем строку с данными
        data['sex'] = 'male' if data['sex'] == 0 else 'female'
        msg = ""
        for key in ["header", "first_name", "last_name", "sex", "age", "email", "city"]:
            if key == 'header':
                # Если ключ - header, используем значение напрямую
                res = Translated_Language.return_translated_text(key, id_=user_id_msg)
            else:
                # Форматируем строку с данными
                res = Translated_Language.return_translated_text(
                    key, id_=user_id_msg
                ).format(**data)
            msg += res
        return msg

class ControllText(Translated_Language):
    control_sex: list = ['male', 'female', 'мужской', 'женский', 'maschile', 'femminile']
    def control(self, word, user_id_msg):
        if word in ControllText.control_sex:
            return ControllText.return_translated_text(word, id_ = user_id_msg)