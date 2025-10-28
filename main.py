import logging
import os
from pathlib import Path
from ai import ask_gemini
import telebot
from telebot import apihelper
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from keep_alive import keep_alive

# فعال کردن نگهدارنده
keep_alive()

apihelper.ENABLE_MIDDLEWARE = True
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set")

bot = telebot.TeleBot(API_TOKEN)

# هندلرهای شما...
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'hello welcome to my bot')

@bot.message_handler(content_types=['text'])
def echo(message):
    prompt = message.text
    answer = ask_gemini(prompt, "AI_API_KEY")
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types=['photo', 'video', 'audio', 'document', 'sticker', 'stickers', 'voice'])
def echo(message):
    bot.send_message(message.chat.id,"متاسفانه من یک ربات متنی هستم و فعلا قابلیت تولید یا خواندن فایل ها رو ندارم")
    bot.send_message(message.chat.id, "دیگه چه کاری از دستم بر میاد برات انجام بدم")

print("bot is running")
bot.infinity_polling()