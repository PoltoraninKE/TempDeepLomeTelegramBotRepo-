import base64

import requests
from telegram import Contact
import json
from telegram import File


class BackendRequester:
    def __init__(self, url: str):
        self.url = url
        # Отключил пока не разберусь с SSL
        self.verify = False
        self.headers = {'content-type': 'application/json'}

    # Зарегистрировать пользователя в базе
    def register(self, contact: Contact) -> bool:
        print("Registering user")
        data = {
            "Id": 0,
            "FirstName": contact.first_name,
            "LastName": contact.last_name,
            "UserId": contact.user_id,
            "Phone": contact.phone_number,
            "Events": [
            ],
            "Trashes": [
            ]
        }
        print(data)
        try:
            response = requests.post(self.url + "/add_user", json=data,
                                     headers=self.headers, verify=self.verify)
            print(response)
            if response.status_code == 200:
                return True
            return False
        except Exception as ex:
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
                          headers=self.headers, verify=self.verify)
        print(r.status_code)

    def healthcheck(self) -> bool:
        print(self.url + "/health_check")
        response = requests.get(url=self.url + "/health_check", verify=self.verify)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_registered_users(self):
        try:
            response = requests.get(url=self.url + "/get_all_users")
        except Exception as ex:
            print(ex)
        return response.content

    def send_photo(self, file: File):
        byte_array = file.download_as_bytearray()
        test = base64.b64encode(byte_array)
        new_str = test.decode('utf-8')

        requests.post(self.url + "/try_in_photo", json=new_str)

    # Зарегистрировать евент в базе
    def new_event(self, user_location: str):
        url_add_event = self.url + '/add_event'
        response = requests.post(url=url_add_event, json=)
