import telebot
from decouple import config

from src.services.tgbot import BotService

botToken = config('BOT_TOKEN')
bot = telebot.TeleBot(botToken)
bot_service = BotService(bot)


@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.id)
    bot_service.start(message.from_user.id)


@bot.message_handler(content_types=['text'])
def func(message):
    bot_service.message_handler(message, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
