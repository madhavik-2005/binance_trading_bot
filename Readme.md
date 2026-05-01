# 📊 Binance Futures Trading Bot (Testnet)

A Python-based trading bot that interacts with Binance Futures Testnet (USDT-M).
Supports MARKET, LIMIT, and STOP_MARKET orders with both CLI and Streamlit dashboard.

---

# 🚀 Features

* ✅ Place MARKET orders (instant execution)
* ✅ Place LIMIT orders (price-based execution)
* ✅ Place STOP_MARKET orders (trigger-based orders)
* ✅ CLI-based trading interface
* ✅ Streamlit dashboard UI
* ✅ Live market price integration
* ✅ Input validation (price, quantity, notional value)
* ✅ Logging of API requests and responses
* ✅ Robust error handling

---

# 🏗️ Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py          # Binance client setup
│   ├── orders.py          # Order execution logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
│
├── cli.py                 # CLI interface
├── app.py                 # Streamlit dashboard
├── trading_bot.log        # Log file
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup Instructions (Mac)

## 1. Clone Repository

```
git clone <your_repo_url>
cd trading_bot
```

---

## 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 4. Add API Keys

Create a `.env` file in the root folder:

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_secret
```

Get keys from Binance Futures Testnet:
https://testnet.binancefuture.com

---

# ▶️ How to Run

---

## 🖥️ CLI Mode

### MARKET Order

```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

### LIMIT Order

```
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 78000
```

---

### STOP_MARKET Order

```
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.002 --price 76000
```

---

## 🌐 Streamlit Dashboard

```
streamlit run app.py
```

Open in browser:
http://localhost:8501

---

# 📊 Order Types Explained

### 🔹 MARKET

* Executes immediately at current market price

### 🔹 LIMIT

* Executes only when price reaches specified level

### 🔹 STOP_MARKET

* Trigger-based order
* Activates when price crosses target
* Uses `algoId` instead of `orderId`

---

# ⚠️ Errors Faced & Fixes

---

### 1. Limit Price Error

```
Limit price can't be lower than market
```

✔ Fix: Use price near market value

---

### 2. Minimum Notional Error

```
Order must be ≥ 100 USDT
```

✔ Fix: Increase quantity
Example:

```
0.002 BTC ≈ 150 USDT
```

---

### 3. STOP Order Missing orderId

✔ Cause:

* STOP orders return `algoId`

✔ Fix:

```
order["orderId"] = order["algoId"]
order["status"] = order["algoStatus"]
```

---

### 4. Streamlit Tuple Error

```
'tuple' object has no attribute 'get'
```

✔ Fix:

```
order, live_price = place_order(...)
```

---

### 5. API Endpoint Issue

```
Failed to resolve api.binance.com
```

✔ Fix:

```
Client(..., testnet=True)
```

---

# 📁 Logs

All logs stored in:

```
trading_bot.log
```

Includes:

* Order request
* API response
* Final status

---

# 🧠 Design Decisions

* Modular architecture (client, orders, validators)
* Separation of concerns
* API response normalization
* Pre-validation before API calls
* Logging for debugging

---

# 🚀 Future Improvements

* Price charts (like trading apps)
* Order history tracking
* AI-based trading signals
* Cloud deployment enhancements


---

# 📸 Suggested Screenshots

* MARKET order (FILLED)
* LIMIT order (PENDING)
* STOP order (ACTIVE)
* Streamlit dashboard

---

# 👩‍💻 Author

Madhavi
CSE (AI & DS), IIIT Kottayam
