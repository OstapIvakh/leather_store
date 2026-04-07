import os
from dotenv import load_dotenv
import requests

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML" # Дозволяє робити текст жирним тощо
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
