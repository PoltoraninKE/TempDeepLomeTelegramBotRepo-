from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from EventCreationModel import EventCreationModel
from backend_service import BackendService
import resources as res

class UserMessageHandler:

    current_event_model: EventCreationModel

    def __init__(self, backend_requester: BackendService):
        self.backend_requester = backend_requester
        #self.registered_users = self.get_registered_users()
        self.path_to_save_file = "C:\\Users\\Kirul\\Desktop\\DeepLome\\TempDeepLomeTelegramBotRepo-\\users_images"

    # (/start)
    def start(self, update: Update) -> None:
<<<<<<< HEAD
        update.message.reply_text("""
            Приветствую! Меня зовут TrashFinder_Bot, я готов стать вашим путеводителем по нашей экологической карте.
- Для того, чтобы зарегистрироваться в системе введите команду - /register
- Для создания нового ивента введите команду - /new_event
- Для того, чтобы понять что вообще тут происходит введите команду /help
- Для просмотра, что у нас есть на карте перейдите скачайте мобильное приложение или посмотрите на нашем сайте.
            """)
=======
        update.message.reply_text(res.START_TEXT)
>>>>>>> bf352a4a939490b3585c2c826dbef11c11b2aa9e

    # (/help)
    def help_info(self, update: Update) -> None:
        update.message.reply_text(res.HELP_COMMAND_TEXT)

    # (/registration)
    # TODO Вынести строки в отдельный ресурсный файл
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

        save_file_path = self.path_to_save_file + str(user_chat_id) + '_' + file.file_name

        # Качаем файл на файловую шару
        obj = context.bot.get_file(file.file_id)
        obj.download(
            custom_path=save_file_path)

        self.current_event_model = EventCreationModel()
        self.current_event_model.user = update.message.from_user
        self.current_event_model.event_photo = obj

<<<<<<< HEAD
        # Тут проверка на то, что у нас находится на картинке
        update.message.reply_text("Ищем мусор на фотографии, пожалуйста подождите")

        my_keyboard = [

            [KeyboardButton(text='Местоположение', request_location=True)]
        ]
        markup = ReplyKeyboardMarkup(keyboard=my_keyboard)
        update.message.reply_text(text=
                                  "Для создания ивента нам требуется ваше местоположение. Пожалуйста, поделитесь им :)",
                                  reply_markup=markup)

=======
>>>>>>> bf352a4a939490b3585c2c826dbef11c11b2aa9e
        # Отправляем файл на бекенд, если нужный тип, иначе говорим, что что-то пошло не так.
        if file.mime_type == 'image/jpeg':
            # Check 4 good photo
            response = self.backend_requester.send_photo(obj)
            if response.status_code == 200:
                self.share_location(update)
            else:
                print(response.raw)
                update.message.reply_text(
                    text="Произошла ошибка на сервере, пожалуйста обратитесь за помощью к администрации проекта.")
        else:
            update.message.reply_text(text="""
                        Данный тип фото не поддерживается, пожалуйста пришлите его в следующих форматах: 
                        - jpeg
                        """)

    def get_user_location(self, update: Update) -> None:
        user_location_json = update.message.location.to_json()
        self.current_event_model.user_location = update.message.location
        send_str = "Вы поделились вашим местоположением: " + user_location_json
        update.message.reply_text(text=send_str)
<<<<<<< HEAD
        update.message.reply_text(
            "Субботник зарегистрирован! Спасибо, что помогаете сделать этот мир чуточку лучше.")
        self.backend_requester.new_event(self.current_event_model.user, self.current_event_model.user_location, self.current_event_model.event_photo)
=======
        print("User: ")
        print(self.current_event_model.user)
        print("Photo: ")
        print(self.current_event_model.event_photo)
        print("Location: ")
        print(self.current_event_model.user_location)
        self.backend_requester.new_event(self.current_event_model)
>>>>>>> bf352a4a939490b3585c2c826dbef11c11b2aa9e


    def photo_in_message(self, update: Update) -> None:
        update.message.reply_text(text="Пожалуйста, пришлите не сжатое фото, мы не можем обработать сжатое :(")

    def get_registered_users(self) -> bytes:
        return self.backend_requester.get_registered_users()

    def new_event(self, update: Update, context: CallbackContext) -> None:
<<<<<<< HEAD
        update.message.reply_text(text=
                                  """Отлично, вы хотите зарегистрировать субботник! Поделитесь, пожалуйста фотографией, места, которое нужно убрать.
Поставьте галочку "без сжатия", чтобы мы могли корректно обработать фотографию""")
=======
        update.message.reply_text(text="""Отлично, вы хотите зарегистрировать субботник! Поделитесь, пожалуйста 
        фотографией, места, которое нужно убрать. Поставьте галочку "без сжатия", чтобы мы могли корректно обработать 
        фотографию""")

    # Здесь нужно:
    #   1. Проверить зарегистрирован ли пользователь
    #   2. Показать список ивентов, которые есть
    #   3. При нажатии зарегистрировать пользователя в этот ивент
    #   *. Полистать список (ВОЗМОЖНО)
    def join_to_event(self, update: Update, context: CallbackContext) -> None:
        self.backend_requester.is_user_registered(update.message.from_user.id)
>>>>>>> bf352a4a939490b3585c2c826dbef11c11b2aa9e
