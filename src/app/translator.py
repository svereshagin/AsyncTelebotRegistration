from typing import Optional, Any
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
from src.bot_instance import i18n


class Translated_Language:
    # Словарь для хранения информации о языке пользователя
    _ = i18n.gettext
    LANGUAGES = ["French", "Русский", "Italiano", "English", "Spanish"]
    ACRONYMS = ["fr", 'ru', 'it', 'en', 'es']
    users_lang = {}


    BUTTONS = {
        "yes": _("yes"),
        "no": _("no"),
        "accept": _("accept"),
        "reject": _("reject"),
        "show_rules_question": _("show_rules_question"),
        "you agreed": _("you agreed"),
        "you declined": _("you declined"),
        "male": _("male"),
        "female": _("female"),
        "choose_sex": _("Choose your sex:"),
        "keyboards": {
            "menu": _("menu"),
            "help": _("help"),
            "cancel": _("exit"),
            "lang": _("language"),
            "show_rules": _("agreement"),
            "profile": _("profile"),
        }
    }
    REGISTRATION = {
        "greetings": {
            "start": _("Hello! Proceed with the registration\nYou can skip the process with /cancel command.\n"
                       "Also you can return to registration with\n /registration or /start commands"),
            "already_registered": _("You are already registered"),
            "language_changed": _("Language has been changed",),
        },
        "prompts": {
            "ask_language": _("What is your language?"),
            "ask_name": _("What is your name?"),
            "ask_last_name": _("What is your last name?"),
            "choose_sex": _("Choose your sex:"),
            "ask_age": _("What is your age?"),
            "ask_email": _("What is your email?"),
            "ask_city": _("What is your city?"),
        },
        "responses": {
            "male": _("male"),
            "female": _("female"),
            "data_received": _("Data received"),
            "age_incorrect": _("Age incorrect"),
            "cancel_command": _("Cancel command"),
            "user_data": _("User data"),
        },
        "errors": {
            "Error": _("Error"),
        },
        "user_data": _("Your profile data: \n"
        "name - {name}\n"
        "lastname - {last_name}\n"
        "sex - {sex}\n"
        "age  -   {age}\n"
        "email - {email}\n"
        "city  -   {city}\n"
        "language  -   {language}\n")
    }


    @staticmethod
    def get_translation(dict_: str, key: str, lang: Optional[str] = None) -> str:
        """
        Извлекает перевод из вложенного словаря на основе переданного ключа.

        Args:
            dict_ (str): Имя словаря: REG || BUTT
            key (str): Ключ в формате "category.subcategory.key".
            lang (Optional[str]): Язык перевода. Если не передан, используется "en".

        Returns:
            str: Переведенный текст.
        """
        lang = lang or "en"
        keys = key.split(".")  # Разделяем ключ по точке

        if dict_ == 'REG':
            current_dict: Any = Translated_Language.REGISTRATION
        elif dict_ == 'BUTT':
            current_dict: Any = Translated_Language.BUTTONS
        try:
            for k in keys:
                current_dict = current_dict[k]
            # Возвращаем перевод с учетом языка
            return i18n.gettext(current_dict, lang=lang)
        except KeyError:
            return f"Translation for '{key}' not found."

    @classmethod
    def translate(cls, dict_, key: str, user_id: Optional[int] = None) -> str:
        """
        Перевод текста для конкретного пользователя по ключу.

        Args:
            key (str): Ключ для перевода.
            user_id (Optional[int]): ID пользователя.

        Returns:
            str: Переведенный текст.
        """
        lang = cls.users_lang.get(user_id, "en")  # Получаем язык пользователя
        return cls.get_translation(dict_, key, lang=lang)
    @classmethod
    def languages_keyboard(self):
        # Создаем клавиатуру с кнопками для выбора языка
        keyboard = [
            [InlineKeyboardButton(text=lang, callback_data=acronym) for lang, acronym in
             zip(Translated_Language.LANGUAGES, Translated_Language.ACRONYMS)]
        ]

        return InlineKeyboardMarkup(keyboard)