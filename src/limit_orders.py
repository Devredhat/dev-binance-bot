from bot_base import BasicBot
import sys
import argparse

def get_step_size(bot, symbol):
    if args.test:
        return 0.001
    exchange_info = bot.safe_call(bot.client.futures_exchange_info)
    if not exchange_info:
        return 0.001
    for sym in exchange_info['symbols']:
        if sym['symbol'] == symbol:
            for filt in sym['filters']:
                if filt['filterType'] == 'LOT_SIZE':
                    return float(filt['stepSize'])
    return 0.001

def check_balance(bot, symbol):
    if args.test:
        print("TEST MODE: Simulated balance 1000 USDT – Proceeding!")
        bot.logger.info("TEST MODE: Balance bypassed")
        return True
    account = bot.safe_call(bot.client.futures_account)
    if not account:
        return False
    usdt_balance = next((float(a['availableBalance']) for a in account['assets'] if a['asset'] == 'USDT'), 0)
    print(f"USDT Available Balance: {usdt_balance}")
    if usdt_balance < 10:
        print("⚠️ Low balance! Transfer more USDT to Futures wallet.")
        bot.logger.warning("Low USDT balance for order")
        return False
    positions = [p for p in account['positions'] if p['symbol'] == symbol]
    if positions:
        print(f"Current Position: {positions[0]['positionAmt']} {symbol}")
    else:
        print("No open position – will open new.")
    return True

def validate_and_round(symbol, side, qty, price):
    symbol = symbol.upper()
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL")
    try:
        q = float(qty)
        p = float(price)
        if q < 0.001 or p <= 0:
            raise ValueError("Quantity min ~0.001, price >0")
    except ValueError:
        raise ValueError("Quantity/price must be positive numbers")
    if not symbol.endswith('USDT'):
        raise ValueError("Symbol must end with USDT")
    return symbol, side, str(round(q, 3)), str(round(p, 2))

def place_limit_order(bot, symbol, side, qty, price):
    if not check_balance(bot, symbol):
        return None
    
    try:
        symbol, side, qty, price = validate_and_round(symbol, side, qty, price)
        step_size = get_step_size(bot, symbol)
        rounded_qty = str(round(float(qty) / step_size) * step_size)
        print(f"Auto-rounded qty to {rounded_qty} (step size: {step_size})")
    except ValueError as e:
        print(f"Validation Error: {e}")
        bot.logger.error(f"Limit validation fail: {e}")
        return None
    
    if args.test:
        print("TEST MODE: Simulating limit order ...")
        simulated_order = {'orderId': 888888, 'status': 'NEW'}
        bot.logger.info(f"SIMULATED Limit order: {simulated_order}")
        print("🎉 SIMULATED Limit Order Placed Successfully!")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {rounded_qty}")
        print(f"Limit Price: ${price}") 
        print(f"Order ID: {simulated_order['orderId']}")
        print(f"Status: {simulated_order['status']} (Pending until price hit)")
        return simulated_order
    
    # Real leverage
    leverage_set = bot.safe_call(bot.client.futures_change_leverage, symbol=symbol, leverage=1)
    if not leverage_set:
        print("⚠️ Leverage set failed.")
        return None
    print("Leverage set to 1x.")
    bot.logger.info(f"Leverage set to 1x for {symbol}")
    
    # Real order
    order = bot.safe_call(
        bot.client.futures_create_order,
        symbol=symbol,
        side=side,
        type='LIMIT',
        timeInForce='GTC',
        quantity=rounded_qty,
        price=price
    )
    if order:
        print("🎉 Limit Order Placed Successfully!")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {rounded_qty}")
        print(f"Limit Price: ${price}")
        print(f"Order ID: {order['orderId']}")
        print(f"Status: {order['status']} (Pending until price hit)")
        bot.logger.info(f"Limit order placed: ID {order['orderId']}, Price {price}")
        return order
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Limit Orders Bot")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity e.g., 0.001")
    parser.add_argument("price", help="Price e.g., 70000")
    parser.add_argument("--test", action="store_true", help="Simulate order")
    args = parser.parse_args()
    
    bot = BasicBot()
    place_limit_order(bot, args.symbol, args.side, args.quantity, args.price)