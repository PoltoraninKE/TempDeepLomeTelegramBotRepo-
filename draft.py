
def coordinates_to_address(coordinate):
    PARAMS = {
        "apikey": "48e09196-f569-46b6-94b3-6a58ea30c178",
        "format": "json",
        "lang": "ru_RU",
        # Точность в API Яндекса - "Точки до дома"
        "kind": "house",
        "geocode": coordinate
    }
    try:
        req = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = req.json()
        address_string = json_data["response"][
            "GeoObjectCollection"][
            "featureMember"][
            0][
            "GeoObject"][
            "metaDataProperty"][
            "GeocoderMetaData"][
            "AddressDetails"][
            "Country"][
            "AddressLine"]
        return address_string
    except Exception as exp:
        return "Wrong message, try different"


    # coordinate = update.message.text
    # address_string = coordinates_to_address(coordinate)
    # print(address_string)
    # update.message.reply_text(address_string)