from flask import Flask, request
import logging
import os
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from ai import ask_gemini
import telebot
from telebot import apihelper
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

# تنظیمات Flask
app = Flask(__name__)

# تنظیمات Telegram Bot
apihelper.ENABLE_MIDDLEWARE = True
API_TOKEN = "8224216936:AAFcLtbxgHTi6coPa5mvdH8wS0x1VQ4H_qY"

bot = telebot.TeleBot(API_TOKEN)

# ذخیره چت‌های فعال
active_chats = set()


def send_ping_to_all():
    """ارسال پیام ping به تمام چت‌های فعال"""
    if not active_chats:
        print("No active chats to ping")
        return

    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🤖 پینگ خودکار ربات (Flask)\n⏰ زمان: {current_time}\n✅ ربات در حال اجراست"

    for chat_id in list(active_chats):
        try:
            bot.send_message(chat_id, message)
            print(f"Ping sent to {chat_id}")
        except Exception as e:
            print(f"Failed to send ping to {chat_id}: {e}")
            active_chats.discard(chat_id)


# تنظیم scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=send_ping_to_all,
    trigger=IntervalTrigger(minutes=5),
    id='ping_job',
    name='Send ping every 5 minutes',
    replace_existing=True
)
scheduler.start()


# routes Flask
@app.route('/')
def home():
    return "Bot is running with Flask!"


@app.route('/health')
def health():
    return {"status": "healthy", "active_chats": len(active_chats)}


@app.route('/send_test/<chat_id>')
def send_test(chat_id):
    try:
        bot.send_message(chat_id, "تست از طریق Flask")
        return f"Message sent to {chat_id}"
    except Exception as e:
        return f"Error: {e}"


# handlers Telegram Bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    active_chats.add(message.chat.id)
    bot.send_message(message.chat.id, 'سلام به هوش مصنوعی میتنی بر متن BylAI خوش آمدید')
    bot.send_message(message.chat.id, 'Hello and welcome to the text-based AI BylAI')


@bot.message_handler(commands=['ping'])
def ping_command(message):
    active_chats.add(message.chat.id)
    bot.send_message(message.chat.id, 'شما در لیست دریافت پینگ خودکار قرار گرفتید')


@bot.message_handler(commands=['stop_ping'])
def stop_ping_command(message):
    active_chats.discard(message.chat.id)
    bot.send_message(message.chat.id, 'شما از لیست دریافت پینگ خودکار حذف شدید')


@bot.message_handler(content_types=['text'])
def echo(message):
    active_chats.add(message.chat.id)
    prompt = message.text
    answer = ask_gemini(prompt, "AIzaSyCtrFeQ16pW-WPzcUpp-N-IB1LwcmsaVlk")
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['photo', 'video', 'audio', 'document', 'sticker', 'stickers', 'voice'])
def echo(message):
    active_chats.add(message.chat.id)
    bot.send_message(message.chat.id, "متاسفانه من یک ربات متنی هستم و فعلا قابلیت تولید یا خواندن فایل ها رو ندارم")
    bot.send_message(message.chat.id, "دیگه چه کاری از دستم بر میاد برات انجام بدم")


def run_bot():
    """اجرای ربات در thread جداگانه"""
    print("Telegram bot is running with Flask")
    bot.infinity_polling()


if __name__ == '__main__':
    import threading

    # اجرای ربات در thread جداگانه
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # اجرای Flask
    print("Flask app is running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)