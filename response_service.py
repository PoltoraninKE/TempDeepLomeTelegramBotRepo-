import json
from telegram import Location, User


# Тут нужно сделать сервис, который будет принимать модели, делать из них нужные и отправлять ответом готовый json

def event_json(location: Location, user: User) -> str:
    dict_location = location.to_dict()
    dict_user = user.to_dict()

    # Конкатим два словаря и дампим их в джейсоне
    return json.dumps({**dict_location, **dict_user})


# Сделать нормальную связку пользователь -> мусорка (ивент), чтобы не было проблем со связкой в базе.

def user_json(user: User) -> str:
    return json.dumps(user)

