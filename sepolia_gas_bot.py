from web3 import Web3
import os, requests
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))

def main():
    # 1️⃣ Fetch Wei price
    price_wei = w3.eth.gas_price                  # Wei from RPC :contentReference[oaicite:4]{index=4}

    # 2️⃣ Convert to Gwei using correct helper
    price_gwei = w3.from_wei(price_wei, "gwei")   # snake_case :contentReference[oaicite:5]{index=5}

    # 3️⃣ Send Telegram message
    msg = f"⛽ Sepolia Gas Price: {price_gwei} Gwei"
    resp = requests.post(
        f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",  # API docs :contentReference[oaicite:6]{index=6}
        data={"chat_id": os.getenv("TELEGRAM_CHAT_ID"), "text": msg}
    )
    resp.raise_for_status()

if __name__ == "__main__":
    main()
