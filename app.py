import requests
import json

TOKEN = ""

url = f'https://api.telegram.org/bot{TOKEN}/'


def get_help_text():
    return """
/start - Botni ishga tushirish
/help - Bot haqida ma'lumot
/remove - Buttonlarni olib tashlash 
/info - Biz haqimizda
                """


def get_location():
    from geopy.geocoders import Nominatim

    # Initialize geocoder
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Get current location

    location = geolocator.geocode(" Uzbekistan, Tashkent, Yunusabad")
    print(location)
    # Print latitude and longitude
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
    return {
        'latitude': location.latitude,
        'longitude': location.longitude
    }


def make_request(method, parametres: dict = None):
    response = requests.get(f'{url}{method}', params=parametres)
    return response.json()


def get_updates(offset) -> dict:
    return make_request('getUpdates', parametres={"offset": offset})


def send_message(chat_id: int, text: str, reply_markup=None):
    make_request('sendMessage', {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": reply_markup})


# def send_location(chat_id, latitude, longitude):
#     make_request('sendLocation', {
#         'chat_id': chat_id,
#         'latitude': latitude,
#         'longitude': longitude,
#     })
#
#
# def send_contact(chat_id, phone_number, first_name):
#     make_request('sendContact', {
#         'chat_id': chat_id,
#         'phone_number': phone_number,
#         'first_name': first_name
#     })


def send_media_group(chat_id, media):
    make_request('sendMediaGroup', {
        'chat_id': chat_id,
        'media': json.dumps(media)
    })


def get_reply_markup(resize: bool = False, one_time: bool = False):
    reply_markup = {
        "keyboard": [
            [{"text": "help"}, {"text": "remove"}],
            [{"text": "location", "request_location": True},
             {"text": "contact", "request_contact": True}],
        ],
        "resize_keyboard": resize,
        "one_time_keyboard": one_time
    }
    return json.dumps(reply_markup)


if __name__ == '__main__':
    offset = 0
    while True:
        try:
            updates = get_updates(offset)
        except Exception as e:
            raise Exception(e)

        result_list = updates.get('result')
        for update in result_list:
            offset = update.get('update_id') + 1
            # print('\n')
            # print(update)
            # print('\n')
            try:
                text = update["message"]["text"]
            except Exception as e:
                print(e)
                text = "None"
            chat_id = update["message"]["chat"]["id"]
            first_name = update["message"]["chat"]["first_name"]

            if text == "/start":
                reply_markup = get_reply_markup(resize=True)
                send_text = f"Assalomu alaykum, {first_name}\n/help - barcha buyruqlar ro'yxati"
                send_message(chat_id, send_text, reply_markup)

            if text in ("/help", "help"):
                send_text = get_help_text()
                send_message(chat_id, send_text)

            if text in ("/remove", "remove"):
                send_text = "Buttonlar olib tashlandi"
                send_message(chat_id, send_text, reply_markup='{"remove_keyboard": true}')

            if text in ("/info", "info"):
                send_media_group(chat_id, media=[
                    {'type': 'photo',
                     'media': 'https://core.telegram.org/file/464001434/100bf/eWprjdgzEbE.100386/644bbea83084f44c8f'},
                    {'type': 'photo',
                     'media': 'https://ioflood.com/blog/wp-content/uploads/2023/09/Collage-of-Python-programming-aspects-syntax-libraries-Python-symbols-logo.jpg',
                     "caption": "https://python.org/"},
                ])

