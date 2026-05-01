def validate_order(symbol, side, order_type, quantity, price=None):

    # 🔹 Symbol
    if not symbol or not symbol.endswith("USDT"):
        raise ValueError("Only USDT pairs supported (e.g., BTCUSDT)")

    # 🔹 Side
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    # 🔹 Order Type
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET")

    # 🔹 Quantity
    try:
        quantity = float(quantity)
    except:
        raise ValueError("Quantity must be numeric")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    # 🔹 Price validation
    if order_type in ["LIMIT", "STOP_MARKET"]:
        if price is None:
            raise ValueError("Price required for LIMIT and STOP_MARKET")

        try:
            price = float(price)
        except:
            raise ValueError("Price must be numeric")

        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
    # 🔹 Minimum notional check (approx)
    if order_type in ["LIMIT", "STOP_MARKET"]:
        notional = float(quantity) * float(price)

        if notional < 100:
            raise ValueError(
                f"Order value too small (~{notional:.2f} USDT). Minimum is 100 USDT. Increase quantity."
            )