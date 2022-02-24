import requests
from telegram import Contact


class BackendRequester:
    def __init__(self, url):
        self.url: str = url

    # Зарегистрировать пользователя в базе
    def register_user(self, contact: Contact) -> bool:
        data = {
            "Id": None,
            "FirstName": contact.first_name,
            "LastName": contact.last_name,
            "UserId": contact.user_id,
            "Phone": contact.phone_number,
            "Trashes": [
            ]
        }
        try:
            response = requests.post(self.url + "/bot/new_user", json=data,
                                     headers={'content-type': 'application/json'})
            if response.status_code == 200:
                print(response)
                return True
            return False
        except Exception as ex:
            print(response)
            print(ex)
            return False

    # Отправить инфу о мусорке (!!! Спросить на работе какие есть варианты !!!
    # или можно просто сделать разными запросами или еще как...)
    def send_trash_info(self, user_id, longitude, latitude, picture_in_bytes):
        byte_str = str(picture_in_bytes).replace('bytearray(b', '')
        str1 = bytes(picture_in_bytes)
        print(str1)
        picture_as_str = str1.decode()  # .replace("'", '"')[1, -1]
        print(picture_as_str)
        data = {
            "Id": None,
            "TelegramId": user_id,
            "Trashes": {
                "Id": None,
                "UserId": user_id,
                "Longitude": longitude,
                "Latitude": latitude,
                "Photo": picture_as_str
            }
        }
        print(str(picture_in_bytes))
        print(json.dumps(data))
        r = requests.post("http://localhost:13424/bot/new_user", json=data,
                          headers={'content-type': 'application/json'})
        print(r.status_code)

    def healthcheck(self) -> bool:
        response = requests.get(url=self.url)
        if response.status_code == 200:
            return True
        else:
            return False

    # Зарегистрировать евент в базе
    def new_event(self):
        pass
