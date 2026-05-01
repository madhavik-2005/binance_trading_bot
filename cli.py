import argparse
import logging
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger


def display_dashboard(order, args, live_price):
    print("\n" + "="*60)
    print("📊 TRADING BOT DASHBOARD")
    print("="*60)

    print(f"📌 Symbol          : {args.symbol}")
    print(f"📌 Side            : {args.side}")
    print(f"📌 Order Type      : {args.type}")
    print(f"📌 Quantity        : {args.quantity}")

    if args.type in ["LIMIT", "STOP_MARKET"]:
        print(f"📌 Target Price    : {args.price}")

    print("-"*60)
    print(f"💹 Live Price      : {live_price}")
    print("-"*60)

    order_id = order.get("orderId")
    status = order.get("status")

    # 🔥 SMART DISPLAY LOGIC

    # STOP ORDER
    if args.type == "STOP_MARKET":
        print(f"🆔 Order ID        : {order_id}")
        print(f"📈 Status          : {status}")
        print("🟡 STOP ORDER ACTIVE")
        print(f"⏳ Will trigger at price {args.price}")

    # FILLED ORDER
    elif status == "FILLED":
        print(f"🆔 Order ID        : {order_id}")
        print(f"📈 Status          : {status}")
        print("🟢 EXECUTION       : COMPLETED")
        print(f"💰 Avg Price       : {order.get('avgPrice')}")
        print(f"📦 Filled Qty      : {order.get('executedQty')}")

    # PENDING LIMIT
    elif status in ["NEW", "PARTIALLY_FILLED"]:
        print(f"🆔 Order ID        : {order_id}")
        print(f"📈 Status          : {status}")
        print("🟡 EXECUTION       : PENDING")

        if args.type == "LIMIT":
            print(f"⏳ Will execute when price reaches {args.price}")

    else:
        print("🔴 EXECUTION       : FAILED / UNKNOWN")

    print("="*60)


def main():
    setup_logger()
    logging.info("CLI started")

    parser = argparse.ArgumentParser(description="Trading Bot CLI")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--price", required=False)

    args = parser.parse_args()

    try:
        # ✅ Validate inputs
        validate_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        # ✅ Initialize client
        client = BinanceClient().get_client()

        # ✅ Place order
        order, live_price = place_order(
            client,
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        # ✅ Display dashboard
        display_dashboard(order, args, live_price)

    except Exception as e:
        logging.error(f"CLI Error: {str(e)}")

        print("\n" + "="*60)
        print("❌ ORDER FAILED")
        print("="*60)
        print(f"Reason: {str(e)}")
        print("💡 Tip: Ensure order value ≥ 100 USDT for Binance Futures")
        print("="*60)


if __name__ == "__main__":
    main()