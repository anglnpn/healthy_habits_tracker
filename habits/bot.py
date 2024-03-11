from config.settings import TELEGRAM_BOT_API_TOKEN
import requests


def send_message(chat_id, text):
    """
    Функция принимает id чата и текст сообщения.
    Собирает и отправляет оповещение пользователю.
    """
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_API_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}

    try:
        response = requests.post(url, params=params)
        # Проверяем статус ответа
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
