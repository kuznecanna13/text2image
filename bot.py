import telebot
from config import *
from logic import Text2ImageAPI

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """Привет! Я бот для генерации картинок с помощью искусственного интеллекта. Напиши запрос!""")


@bot.message_handler(func=lambda message: True)
def generate(message):
    prompt = message.text
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]
    api.save_image(images, "image.jpg")
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.infinity_polling()