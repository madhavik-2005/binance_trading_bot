import logging
import time

def place_order(client, symbol, side, order_type, quantity, price=None):
    try:
        logging.info(f"Order Request: {symbol} {side} {order_type} {quantity} {price}")

        # 🔹 Get live market price
        ticker = client.futures_mark_price(symbol=symbol)
        mark_price = float(ticker["markPrice"])
        logging.info(f"Market Price: {mark_price}")

        # 🔹 Validate LIMIT price
        if order_type == "LIMIT":
            price = float(price)

            if side == "SELL" and price < mark_price * 0.9:
                raise ValueError(f"SELL price too low (market ≈ {mark_price})")

            if side == "BUY" and price > mark_price * 1.1:
                raise ValueError(f"BUY price too high (market ≈ {mark_price})")

        # 🔹 Place order
        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )

        elif order_type == "LIMIT":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

        elif order_type == "STOP_MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP_MARKET",
                stopPrice=price,
                quantity=quantity
            )

        logging.info(f"Raw Response: {order}")

        # 🔥 HANDLE RESPONSE TYPES

        # ✅ Case 1: MARKET / LIMIT
        if "orderId" in order:
            time.sleep(2)

            order_status = client.futures_get_order(
                symbol=symbol,
                orderId=order["orderId"]
            )

            logging.info(f"Final Order Status: {order_status}")
            return order_status, mark_price

        # ✅ Case 2: STOP_MARKET (conditional order)
        elif "algoId" in order:
            logging.info("STOP order created successfully")

            # Normalize response for CLI
            order["orderId"] = order.get("algoId")
            order["status"] = order.get("algoStatus", "NEW")

            return order, mark_price

        else:
            raise Exception(f"Unexpected API response: {order}")

    except Exception as e:
        logging.error(f"Order Error: {str(e)}")
        raise