import os
import requests
import time

def get_gas_price():
    api_key = os.getenv('ETHERSCAN_API_KEY')
    url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['result']['ProposeGasPrice']

def send_telegram_message(message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

if __name__ == '__main__':
    gas_price = get_gas_price()
    send_telegram_message(f'Current Sepolia Gas Price: {gas_price} Gwei')
