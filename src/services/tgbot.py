import requests
from decouple import config
from fastapi import status
from telebot import types

START_TEXT = """Это бот для поиска новых хозяев для бездомных животных из популярных приютов Москвы\n\
    Чтобы продолжить, необходимо Нажать на кнопку Start Match"""
START_MATCH = "Start Match"
ACCEPT = "\U00002705"
USER_NOT_FOUND_ERROR = "Для пользователя не найдены данные"
REJECT = "\U0000274C"

S3_URL = config('S3_URL')
API_URL = config('API_URL')
user_vector_db = {}


class BotService:
    def __init__(self, bot):
        self.bot = bot
        self.reject_button = types.InlineKeyboardButton(REJECT)
        self.accept_button = types.InlineKeyboardButton(ACCEPT)
        self.start_match_button = types.InlineKeyboardButton(START_MATCH)

    def add_start_button(self, markup):
        markup.add(self.start_match_button)

    def add_service_button(self, markup):
        markup.add(self.reject_button, self.accept_button)

    def remove_service_button(self, markup):
        markup.delete(self.reject_button, self.accept_button)

    def start(self, user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.add_start_button(markup)
        self.bot.send_message(user_id, text=START_TEXT, reply_markup=markup)

    def message_handler(self, message, message_text):
        user_id = message.from_user.id
        if message_text == REJECT or message_text == START_MATCH:
            if user_id in user_vector_db:
                next_token = user_vector_db[user_id]
            else:
                next_token = 1
            payload = {
                "next_token": str(next_token),
                "user_id": str(user_id)
            }
            url = f'{API_URL}/get_next_pet'
            response = requests.post(url=url, json=payload)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                self.bot.send_message(user_id, text=USER_NOT_FOUND_ERROR)
                self.bot.send_message(user_id, text=START_TEXT, reply_markup=types.ReplyKeyboardRemove())
            else:
                response_json = response.json()
                print(S3_URL+response_json['url'])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                self.add_service_button(markup)
                self.bot.send_photo(user_id, S3_URL + response_json['url'],
                                    reply_markup=markup)
                user_vector_db[user_id] = response_json['next_token']
        elif ACCEPT:
            if user_id in user_vector_db:
                next_token = user_vector_db[user_id]
            else:
                next_token = 1
            payload = {
                "next_token": str(next_token),
                "user_id": str(user_id)
            }
            url = f'{API_URL}/get_pet_contact'
            response = requests.post(url=url, json=payload)
            response_json = response.json()
            print(response_json['info'])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.add_service_button(markup)
            self.bot.send_message(user_id,
                                  text=response_json['info'],
                                  reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.bot.send_message(user_id, text=START_TEXT, reply_markup=markup)

    def send_message(self, user_id, message):
        self.bot.send_message(user_id, text=message)
