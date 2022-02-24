from telegram import Update, ReplyKeyboardMarkup, KeyboardButton

from backend_requester import BackendRequester


class UserMessageHandler:
    def __init__(self, backend_requester: BackendRequester):
        self.backend_requester = backend_requester

    # (/start)
    def start(self, update: Update) -> None:
        update.message.reply_text("""
            Приветствую! Меня зовут TrashFinder_Bot, я готов стать вашим путеводителем по нашей экологической карте.
            Для того, чтобы зарегистрироваться в системе введите команду - КОМАНДА_РЕГИСТРАЦИИ
            Для создания нового ивента есть кнопки ниже
            Для того, чтобы понять что вообще тут происходит введите команду /help
            Для просмотра, что у нас есть на карте перейдите по ссылке или скачайте мобильное приложение.
            """)

    # (/help)
    def help_info(self, update: Update) -> None:
        update.message.reply_text("""
            Мы - команда, которая разрабатывает карту и ЭКО систему вокруг её.
            С помощью данного бота, вы можете:
            - Создавать информацию о мусорках на карте.
            - Создавать информацию о мусоре на карте.
            - Создавать собственные ивенты по уборке мусора.
            Карта мусорок, мусора и ивентов находится по ссылке - *ссылка*
            Если вы администратор, то ссылка на наше мобильное приложение - *ссылка, в которой скачивание дистрибутива*
            """)

    # (/registration)
    def registration(self, update: Update) -> None:
        update.message.reply_text("""
        Мы используем только ту информацию, которую можем вытащить из вашего телеграма, не более.
        """)
        self.share_phone(update)

    def share_location(self, update: Update) -> None:
        my_keyboard = [

            [KeyboardButton(text='Location', request_location=True)]
        ]
        markup = ReplyKeyboardMarkup(keyboard=my_keyboard)
        update.message.reply_text(text=
                                  "Для создания ивента нам требуется ваше местоположение. Пожалуйста, поделитесь им :)",
                                  reply_markup=markup)

    def share_phone(self, update: Update) -> None:
        my_keyboard = [
            [KeyboardButton(text='Phone', request_contact=True)]
        ]
        markup = ReplyKeyboardMarkup(keyboard=my_keyboard)
        update.message.reply_text(
            text="Для регистрации нам потребуется Ваш номер телефона. Пожалуйста, поделитесь им :)",
            reply_markup=markup)

    def register_user(self, update: Update) -> None:
        if self.backend_requester.register(update.message.contact):
            update.message.reply_text(text="Вы были успешно зарегистрированы!")
        else:
            update.message.reply_text(text="Что-то пошло не так, обратитесь к администраторам проекта, чтобы они "
                                           "разобрались в проблеме.")

    def text(self, update: Update):
        update.message.reply_text("""
                    Извините, я не понял, давайте общаться "командами" :).
                    """)
