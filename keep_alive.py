from flask import Flask
from threading import Thread
import requests
import time

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# برای پینگ دوره‌ای (اختیاری)
def ping_self():
    while True:
        try:
            requests.get('MYBOTADDERS')
        except:
            pass
        time.sleep(300)  # هر 5 دقیقه