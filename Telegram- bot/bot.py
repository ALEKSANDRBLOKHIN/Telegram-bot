# bot.py
import telebot
from config import TOKEN
from extensions import BotHandler

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help', 'values'])
def handle_start_help_values(message):
    response = BotHandler.handle_message(message.text)
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = BotHandler.handle_message(message.text)
    bot.send_message(message.chat.id, response)

bot.polling(none_stop=True)
