import os
import requests
from web3 import Web3
from dotenv import load_dotenv

# Load .env variables
load_dotenv()  # python-dotenv :contentReference[oaicite:6]{index=6}

# Environment variables
RPC_URL     = os.getenv("SEPOLIA_RPC_URL")
BOT_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID     = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_gas_price_gwei():
    """
    Uses eth_gasPrice RPC to get current gas price in Gwei.
    """
    wei_price = w3.eth.gas_price         # eth_gasPrice via web3.py :contentReference[oaicite:7]{index=7}
    return w3.fromWei(wei_price, "gwei")

def send_telegram(msg: str):
    """
    Sends msg to Telegram via Bot API.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"  # sendMessage method :contentReference[oaicite:8]{index=8}
    resp = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    resp.raise_for_status()

def main():
    price = get_gas_price_gwei()
    message = f"⛽ Sepolia Gas Price: {price} Gwei"
    send_telegram(message)

if __name__ == "__main__":
    main()
