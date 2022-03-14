from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from telegram.bot import Bot
from backend_requester import BackendRequester
from message_handler import UserMessageHandler

class TrashFinderBot:
    def __init__(self, bot_token) -> None:
        self.backend_requester = BackendRequester(url="http://localhost:5094")
        self.message_handler = UserMessageHandler(self.backend_requester)

        # Установка данных бота
        self.bot = Bot(token=bot_token)
        self.updater = Updater("2006392416:AAHd2COx0-ItWQkmvGRavUzOHTTWhytqiVQ", use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Добавление хендлеров, для бота
        self.register_handlers()

        # Запуск бота
        self.updater.start_polling()
        print('bot was started')
        self.updater.idle()


    def register_handlers(self) -> None:
        self.dispatcher.add_handler(CommandHandler("start", self.on_start))
        self.dispatcher.add_handler(CommandHandler("register", self.on_register))
        self.dispatcher.add_handler(CommandHandler("help", self.on_help))
        self.dispatcher.add_handler(CommandHandler("share_phone", self.on_share_phone))
        self.dispatcher.add_handler(CommandHandler("share_location", self.on_share_location))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.location))
        self.dispatcher.add_handler(MessageHandler(Filters.contact, self.contact))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text))

    # Зарегистрировать пользователя в системе
    def on_register(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.registration(update)

    def healthcheck_API(self):
        self.backend_requester.healthcheck()

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

    # Когда к нам приходит сообщение в виде контакта
    def contact(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.register_user(update)

    # Просто приходит текст какой-либо
    def text(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.text(update)

    # Когда приходит сообщение с локациейы
    def location(self, update: Update, context: CallbackContext) -> None:
        self.message_handler.location(update)
