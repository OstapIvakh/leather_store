import requests

def send_telegram_message(message):
    token = "8687747416:AAFlhIC31VaRhH2rJOLMtYoD7n8aW20Q7lc"
    chat_id = "355907028"
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
