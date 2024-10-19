import telebot
from config import *
from logic import Text2ImageAPI
import os

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """Привет! Я бот для генерации картинок с помощью искусственного интеллекта. Отправь запрос в чат!""")


@bot.message_handler(func=lambda message: True)
def generate(message):
    bot.send_chat_action(message.chat.id, 'typing')
    prompt = message.text
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    bot.send_message(message.chat.id, "Генерирую...")
    images = api.check_generation(uuid)[0]
    api.save_image(images, "image.jpg")
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove('image.jpg')
    bot.delete_message(message.chat.id, message.message_id + 1)


bot.infinity_polling()