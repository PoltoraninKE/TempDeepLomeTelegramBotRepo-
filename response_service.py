import json
from telegram import Location, User, File
import base64


# Тут нужно сделать сервис, который будет принимать модели, делать из них нужные и отправлять ответом готовый json

def event_json(location: Location, user: User, photo: File) -> str:
    file_as_string = file_to_base64_string(photo)
    to_json = {
        "user_id": user.id,
        "user_location": {
            "longitude": location.longitude,
            "latitude": location.latitude
        },
        "photo": file_as_string
    }
    return json.dumps(to_json)

# Сделать нормальную связку пользователь -> мусорка (ивент), чтобы не было проблем со связкой в базе.
# Сделать связку по ID пользователя, который мы можем взять в телеграме, который будет Primary Key'ем.
# По нему ходить в базу и смотреть. Убрать проверку на регистрацию через кэш.


def user_json(user: User) -> str:
    user_photo_as_string = file_to_base64_string(user.get_profile_photos().photos[1])
    to_json = {
        "user_telegram_id": user.id,
        "user_firstname": user.first_name,
        "user_lastname": user.last_name,
        "user_name": user.name,
        "user_photo":
    }
    return json.dumps(to_json)


def file_to_base64_string(file: File):
    file_as_bytearray = file.download_as_bytearray()
    file_in_base64 = base64.b64encode(file_as_bytearray)
    return file_in_base64.decode('utf-8')
