import os
import requests
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

RPC_URL   = os.getenv("SEPOLIA_RPC_URL")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def main():
    price = w3.eth.gas_price               # eth_gasPrice RPC :contentReference[oaicite:3]{index=3}
    gwei  = w3.fromWei(price, "gwei")
    msg   = f"⛽ Sepolia Gas Price: {gwei} Gwei"
    url   = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"  # sendMessage API :contentReference[oaicite:4]{index=4}
    requests.post(url, data={"chat_id":CHAT_ID,"text":msg}).raise_for_status()

if __name__=="__main__":
    main()
