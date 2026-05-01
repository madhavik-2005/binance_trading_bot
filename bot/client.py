import os
from binance.client import Client
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

def get_keys():
    try:
        import streamlit as st
        return st.secrets["API_KEY"], st.secrets["API_SECRET"]
    except:
        return os.getenv("API_KEY"), os.getenv("API_SECRET")

class BinanceClient:
    def __init__(self):
        api_key, api_secret = get_keys()

        self.client = Client(
            api_key,
            api_secret,
            testnet=True
        )

        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def get_client(self):
        return self.client