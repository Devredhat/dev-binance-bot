import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from bot_base import BasicBot
import argparse

def check_balance(bot, symbol):
    if args.test:
        print("TEST MODE: Simulated balance 1000 USDT – Proceeding!")
        bot.logger.info("TEST MODE: Balance bypassed")
        return True
    # Same as above – copy from market/limit
    account = bot.safe_call(bot.client.futures_account)
    if not account:
        return False
    usdt_balance = next((float(a['availableBalance']) for a in account['assets'] if a['asset'] == 'USDT'), 0)
    print(f"USDT Available Balance: {usdt_balance}")
    if usdt_balance < 10:
        print("⚠️ Low balance! Transfer more USDT to Futures wallet.")
        bot.logger.warning("Low USDT balance for order")
        return False
    return True

def validate_oco(symbol, side, qty, price, stop_price, stop_limit_price):
    symbol = symbol.upper()
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL")
    try:
        floats = [float(qty), float(price), float(stop_price), float(stop_limit_price)]
        if any(x <= 0 for x in floats):
            raise ValueError("All values > 0")
    except ValueError:
        raise ValueError("All must be positive numbers")
    if not symbol.endswith('USDT'):
        raise ValueError("Symbol must end with USDT")
    return symbol, side, str(round(float(qty), 3)), str(round(float(price), 2)), str(round(float(stop_price), 2)), str(round(float(stop_limit_price), 2))

def place_oco_order(bot, symbol, side, qty, price, stop_price, stop_limit_price):
    if not check_balance(bot, symbol):
        return None
    
    try:
        symbol, side, qty, price, stop_price, stop_limit_price = validate_oco(symbol, side, qty, price, stop_price, stop_limit_price)
    except ValueError as e:
        print(f"Validation Error: {e}")
        bot.logger.error(f"OCO validation fail: {e}")
        return None
    
    if args.test:
        print("TEST MODE: Simulating OCO order (no API call)...")
        simulated_oco = {'orderListId': 777777}
        bot.logger.info(f"SIMULATED OCO order: {simulated_oco}")
        print("🎉 SIMULATED OCO Order Placed Successfully!")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {qty}")
        print(f"Limit Price (Take-Profit): ${price}")
        print(f"Stop Price (Stop-Loss Trigger): ${stop_price}")
        print(f"Stop Limit Price: ${stop_limit_price}")
        print(f"Order List ID: {simulated_oco['orderListId']}")
        return simulated_oco
    
    # Real leverage
    leverage_set = bot.safe_call(bot.client.futures_change_leverage, symbol=symbol, leverage=1)
    if not leverage_set:
        print("⚠️ Leverage set failed.")
        return None
    print("Leverage set to 1x.")
    bot.logger.info(f"Leverage set to 1x for {symbol}")
    
    # Real OCO
    oco = bot.safe_call(
        bot.client.futures_create_order,
        symbol=symbol,
        side=side,
        type='OCO',
        quantity=qty,
        price=price,
        stopPrice=stop_price,
        stopLimitPrice=stop_limit_price,
        stopLimitTimeInForce='GTC'
    )
    if oco:
        print("🎉 OCO Order Placed Successfully!")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {qty}")
        print(f"Limit Price (Take-Profit): ${price}")
        print(f"Stop Price (Stop-Loss Trigger): ${stop_price}")
        print(f"Stop Limit Price: ${stop_limit_price}")
        print(f"Order List ID: {oco.get('orderListId', 'N/A')}")
        bot.logger.info(f"OCO order placed: List ID {oco.get('orderListId')}")
        return oco
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCO Orders Bot")
    parser.add_argument("symbol", help="Symbol")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity")
    parser.add_argument("price", help="Limit price")
    parser.add_argument("stop_price", help="Stop trigger")
    parser.add_argument("stop_limit_price", help="Stop limit")
    parser.add_argument("--test", action="store_true", help="Simulate")
    args = parser.parse_args()
    
    bot = BasicBot()
    place_oco_order(bot, args.symbol, args.side, args.quantity, args.price, args.stop_price, args.stop_limit_price)