import telebot
from config import TELEGRAM_TOKEN
from ai import ask_openai
from memory import remember, get_history

bot = telebot.TeleBot(TELEGRAM_TOKEN)

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

print("Бот запущен...")
bot.polling(non_stop=True)
