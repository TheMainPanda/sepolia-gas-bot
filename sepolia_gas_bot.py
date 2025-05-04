import os
import requests
from dotenv import load_dotenv

# Load .env into environment (locally) and allow CI to read GitHub Secrets
load_dotenv()  # python-dotenv :contentReference[oaicite:3]{index=3}

# Read credentials from environment
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_sepolia_gas_prices():
    """
    Fetch Sepolia gas prices from Etherscan testnet API.
    """
    url = (
        f"https://api-sepolia.etherscan.io/api"
        f"?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    )  # Sepolia endpoint :contentReference[oaicite:4]{index=4}

    resp = requests.get(url)
    data = resp.json()

    if data.get("status") == "1":
        r = data["result"]
        return {
            "low":     r["SafeGasPrice"],
            "average": r["ProposeGasPrice"],
            "fast":    r["FastGasPrice"]
        }
    else:
        # Print the human‑readable cause (e.g. "Invalid API Key")
        print("Etherscan returned result:", data.get("result"))
        raise ValueError(
            f"Etherscan API error: {data.get('message','No message')} — see printed result"
        )

def send_telegram_message(text: str):
    """
    Send a text message via Telegram Bot API.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"  # sendMessage method :contentReference[oaicite:5]{index=5}
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text":    text
    }
    res = requests.post(url, data=payload)
    if res.status_code != 200:
        # Surface any Telegram API errors
        print("Telegram response:", res.status_code, res.text)
        raise RuntimeError("Failed to send Telegram message")

def main():
    try:
        prices = get_sepolia_gas_prices()
        msg = (
            f"⛽ Sepolia Gas Prices:\n"
            f"Low: {prices['low']} Gwei\n"
            f"Average: {prices['average']} Gwei\n"
            f"Fast: {prices['fast']} Gwei"
        )
        send_telegram_message(msg)
    except Exception as e:
        # Ensure GitHub Actions log shows the error
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
