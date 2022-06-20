from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from telegram.bot import Bot
from backend_service import BackendService
from message_handler import UserMessageHandler


class TrashFinderBot:
    def __init__(self, bot_token) -> None:
        self.backend_requester = BackendService("http://localhost:5094")
        self.message_handler = UserMessageHandler(self.backend_requester)

        # Установка данных бота
        self.bot = Bot(token=bot_token)
        # TODO Вынести токен в отдельный ресурсный файл
        self.updater = Updater("2006392416:AAHd2COx0-ItWQkmvGRavUzOHTTWhytqiVQ", use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Добавление хендлеров, для бота
        self.register_handlers()

        # Запуск бота
        self.updater.start_polling()
        print('bot was started')
        self.updater.idle()

    def register_handlers(self) -> None:
        # TODO Вынести строки в отдельный ресурсный файл
        self.dispatcher.add_handler(CommandHandler("start", self.on_start))
        self.dispatcher.add_handler(CommandHandler("register", self.on_register))
        self.dispatcher.add_handler(CommandHandler("help", self.on_help))
        self.dispatcher.add_handler(CommandHandler("share_phone", self.on_share_phone))
        self.dispatcher.add_handler(CommandHandler("share_location", self.on_share_location))
        self.dispatcher.add_handler(CommandHandler("share_trash_info", self.get_trash_info))
        self.dispatcher.add_handler(CommandHandler("new_event", self.on_new_event))
        self.dispatcher.add_handler(CommandHandler("join_to_event", self.on_join_to_event))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.get_user_location))
        self.dispatcher.add_handler(MessageHandler(Filters.contact, self.contact))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.photo))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text))
        self.dispatcher.add_handler(MessageHandler(Filters.document, self.document))

    # Зарегистрировать пользователя в системе
    def on_register(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.registration(update)

    def healthcheck_API(self):
        self.backend_requester.health_check()

    # Команда "/start"
    def on_start(self, update: Update, context: CallbackContext) -> None:
        try:
            self.healthcheck_API()
        except Exception as ex:
            print(ex)
        self.message_handler.start(update)

    # Команда "/help"
    def on_help(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.help_info(update)

    # Команда "/share_location"
    def on_share_location(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.share_location(update)

    # Команда "/share_phone"
    def on_share_phone(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.share_phone(update)

    def on_new_event(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.new_event(update, context)

    def on_join_to_event(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.join_to_event(update, context)

    # Когда к нам приходит сообщение в виде контакта
    def contact(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.register_user(update)

    # Просто приходит текст какой-либо
    def text(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.text(update)

    # Когда приходит сообщение с локацией
    def get_user_location(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.get_user_location(update)

    def get_trash_info(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.get_trash_info(update)

    def document(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.document_in_message(update, context)

    def photo(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.photo_in_message(update)

