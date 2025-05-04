import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve API keys from environment variables
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_sepolia_gas_prices():
    """
    Fetches current gas prices from the Sepolia testnet via Etherscan API.
    Returns a dictionary with low, average, and fast gas prices.
    """
    url = f"https://api-sepolia.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") == "1":
            result = data["result"]
            return {
                "low": result["SafeGasPrice"],
                "average": result["ProposeGasPrice"],
                "fast": result["FastGasPrice"]
            }
        else:
            raise ValueError(f"Etherscan API error: {data.get('message', 'No message')}")
    except Exception as e:
        raise RuntimeError(f"Error fetching gas prices: {e}")

def send_telegram_message(message):
    """
    Sends a message to the specified Telegram chat using the bot token.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise ValueError(f"Telegram API error: {response.text}")
    except Exception as e:
        raise RuntimeError(f"Error sending Telegram message: {e}")

def main():
    """
    Main function to fetch gas prices and send them via Telegram.
    """
    try:
        gas_prices = get_sepolia_gas_prices()
        message = (
            f"⛽ Sepolia Gas Prices:\n"
            f"Low: {gas_prices['low']} Gwei\n"
            f"Average: {gas_prices['average']} Gwei\n"
            f"Fast: {gas_prices['fast']} Gwei"
        )
        send_telegram_message(message)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
