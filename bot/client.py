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

        if not api_key or not api_secret:
            raise ValueError("❌ API keys missing")

        # 🔥 FIX: disable ping during init
        self.client = Client(api_key, api_secret, ping=False)

        # ✅ NOW override URLs
        self.client.API_URL = "https://testnet.binance.vision/api"
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        # ✅ OPTIONAL: manually test connection
        self.client.ping()

    def get_client(self):
        return self.client