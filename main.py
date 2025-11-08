import telebot
from flask import Flask, request
from config import TELEGRAM_TOKEN
from ai import ask_openai
from memory import remember, get_history
import os

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

URL = os.getenv("RENDER_EXTERNAL_URL") or "https://dimabot-r754.onrender.com"

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return "DimaBot is running!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот DimaBot 🤖. Задай мне любой вопрос!")

@bot.message_handler(func=lambda msg: True)
def chat(message):
    user_id = message.from_user.id
    text = message.text

    remember(user_id, f"Пользователь: {text}")
    prompt = get_history(user_id) + f"\nБот:"
    answer = ask_openai(prompt)

    remember(user_id, f"Бот: {answer}")
    bot.reply_to(message, answer)

if __name__ == "__main__":
    import requests
    bot.remove_webhook()
    bot.set_webhook(url=f"{URL}/{TELEGRAM_TOKEN}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
