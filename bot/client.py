from binance.client import Client
import streamlit as st
import os

class BinanceClient:
    def __init__(self):
        try:
            api_key = st.secrets["API_KEY"]
            api_secret = st.secrets["API_SECRET"]
        except:
            api_key = os.getenv("API_KEY")
            api_secret = os.getenv("API_SECRET")

        # 🔥 Debug check (IMPORTANT)
        if not api_key or not api_secret:
            raise ValueError("API keys not found. Check Streamlit secrets or .env")

        self.client = Client(api_key, api_secret)

        # ✅ FIX: Force TESTNET endpoints
        self.client.API_URL = "https://testnet.binance.vision/api"
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def get_client(self):
        return self.client