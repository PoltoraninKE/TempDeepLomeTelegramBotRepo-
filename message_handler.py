from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from backend_requester import BackendRequester


class UserMessageHandler:
    def __init__(self, backend_requester: BackendRequester):
        self.backend_requester = backend_requester
        self.registered_users = self.get_registered_users()
        self.path_to_save_file = "D:\\Programmin\\Python\\Telegram_Bots\\TrashFinder_Bot\\TempDeepLomeTelegramBotRepo-\\users_images\\"

    # (/start)
    def start(self, update: Update) -> None:
        update.message.reply_text("""
            Приветствую! Меня зовут TrashFinder_Bot, я готов стать вашим путеводителем по нашей экологической карте.
- Для того, чтобы зарегистрироваться в системе введите команду - /register
- Для создания нового ивента есть кнопки ниже
- Для того, чтобы понять что вообще тут происходит введите команду /help
- Для просмотра, что у нас есть на карте перейдите по ссылке или скачайте мобильное приложение.
            """)

    # (/help)
    def help_info(self, update: Update) -> None:
        update.message.reply_text("""
Мы - команда, которая разрабатывает карту и ЭКОсистему вокруг её.
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
        self.registered_users = self.backend_requester.get_registered_users()

    def share_location(self, update: Update) -> None:
        my_keyboard = [

            [KeyboardButton(text='Местоположение', request_location=True)]
        ]
        markup = ReplyKeyboardMarkup(keyboard=my_keyboard)
        update.message.reply_text(text=
                                  "Для создания ивента нам требуется ваше местоположение. Пожалуйста, поделитесь им :)",
                                  reply_markup=markup)

    def share_phone(self, update: Update) -> None:
        my_keyboard = [
            [KeyboardButton(text='Контакт', request_contact=True)]
        ]
        markup = ReplyKeyboardMarkup(keyboard=my_keyboard)
        update.message.reply_text(
            text="Для регистрации нам потребуется Ваш номер телефона. Пожалуйста, поделитесь им :)",
            reply_markup=markup)

    def register_user(self, update: Update) -> None:
        send_str = "Вы поделились своим контактом. Информация которую мы узнали: " + update.message.contact.to_json()
        update.message.reply_text(send_str)
        if self.backend_requester.register_user(update.message.from_user):
            update.message.reply_text(text="Вы были успешно зарегистрированы!")
        else:
            update.message.reply_text(text="Что-то пошло не так, обратитесь к администраторам проекта, чтобы они "
                                           "разобрались в проблеме.")

    def text(self, update: Update):
        print(type(self.registered_users))
        print(self.registered_users)
        update.message.reply_text(text="""
                    Извините, я не понял, давайте общаться "командами" :).
                    """)

    def get_trash_info_from_user(self, update: Update):
        if update.message.contact.phone_number in self.registered_users:
            self.backend_requester.check_trash_info(update)
        else:
            update.message.reply_text(text="""
            Извините, вы не зарегистрированны в системе,
            или произошла ошибка, пожалуйста зарегистрируйтесь, или обратитесь к организаторам проекта.
            """)

    def document_in_message(self, update: Update, context: CallbackContext) -> None:
        user_chat_id = update.message.chat.id
        file = update.message.document

        save_file_path = self.path_to_save_file + str(user_chat_id) + '_' + file.file_name + ".jpg"

        # Качаем файл на файловую шару
        obj = context.bot.get_file(file.file_id)
        obj.download(
            custom_path=save_file_path)

        # Отправляем файл на бекенд, если нужный тип, иначе говорим, что что-то пошло не так.
        if file.mime_type == 'image/jpeg':
            self.backend_requester.send_photo(obj)
        else:
            update.message.reply_text(text="""
                        Данный тип фото не поддерживается, пожалуйста пришлите его в следующих форматах: 
                        - jpeg
                        """)

    def get_user_location(self, update: Update) -> None:
        user_location_json = update.message.location.to_json()
        send_str = "Вы поделились вашим местоположением: " + user_location_json
        update.message.reply_text(text=send_str)
        self.backend_requester.new_event(user_location_json)

    def photo_in_message(self, update: Update) -> None:
        update.message.reply_text(text="Пожалуйста, пришлите не сжатое фото, мы не можем обработать сжатое :(")

    #
    def get_registered_users(self) -> bytes:
        return self.backend_requester.get_registered_users()
