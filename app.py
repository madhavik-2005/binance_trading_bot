import streamlit as st
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate_order

st.title("📊 Trading Bot Dashboard")

client = BinanceClient().get_client()

symbol = st.text_input("Symbol", "BTCUSDT")
side = st.selectbox("Side", ["BUY", "SELL"])
order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_MARKET"])
quantity = st.text_input("Quantity", "0.001")
price = st.text_input("Price (for LIMIT / STOP)", "")

if st.button("Place Order"):

    try:
        validate_order(symbol, side, order_type, quantity, price)

        # 🔥 FIX HERE
        order, live_price = place_order(
            client, symbol, side, order_type, quantity, price
        )

        st.success("✅ Order Placed Successfully")

        st.write("### 📌 Order Details")
        st.write(order)

        st.write("### 💹 Live Market Price")
        st.write(live_price)

        status = order.get("status")

        # 🔥 SMART STATUS DISPLAY
        if order_type == "STOP_MARKET":
            st.warning("🟡 STOP ORDER ACTIVE")
            st.write(f"Will trigger at price {price}")

        elif status == "FILLED":
            st.success("🟢 Order Executed")

        elif status == "NEW":
            st.warning("🟡 Order Pending")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")