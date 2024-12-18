from typing import Optional

from src.bot_instance import i18n
users_lang = {}


class Translated_Language:
    # Словарь для хранения информации о языке пользователя

    # Словарь с переводами
    TRANSLATED = {
        "start_greeting": "Hello! What is your first name?\nYou can skip the process with /cancel command.",
        "already_registered": "You are already registered.",
        "ask_last_name": "What is your last name?",
        "ask_sex": "What is your sex? (male/female)",
        "ask_age": "What is your age?",
        "ask_email": "What is your email?",
        "ask_city": "What is your city?",
        "thank_you": "Thank you for sharing! Here is a summary of your information:\n"
                       "First Name: {first_name}\n"
                       "Last Name: {last_name}\n"
                       "Sex: {sex}\n"
                       "Age: {age}\n"
                       "Email: {email}\n"
                       "City: {city}",
        "incorrect_age": "Please enter a valid number for age.",
        "cancel_message": "Your information has been cleared. Type /start to begin again.",
        "language_changed": "Language has been changed",
    }

    @staticmethod
    def return_translated_text(text_key: str, id_ : Optional[int], lang_call=0) -> str:
        """Метод для возврата переведенного текста на основе ключа.
        :param text_key: текст отправленный для создания
        :param id_ : id пользователя для нахождения пользователя в словаре
        :param lang_call: oprional, just in case of callback_query situation
        """
        if lang_call:
            print(lang_call, 'ok')
            return i18n.gettext(Translated_Language.TRANSLATED.get(text_key, ''), lang=lang_call)
        return i18n.gettext(Translated_Language.TRANSLATED.get(text_key, ''), lang=users_lang.get(id_, 'en'))
