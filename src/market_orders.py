from bot_base import BasicBot
import sys
import argparse  # For --test flag

def get_step_size(bot, symbol):
    """Fetch LOT_SIZE filter for symbol (rounds qty to valid precision)"""
    if args.test:  # Bypass for test
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
    """Check futures balance & positions (debug unknown errors)"""
    if args.test:  # Bypass for test
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

def validate_and_round(symbol, side, qty):
    """Validate + round qty to step size (PDF: quantity thresholds)"""
    symbol = symbol.upper()
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL")
    try:
        q = float(qty)
        if q < 0.001:
            raise ValueError("Quantity too small – min ~0.001 for BTCUSDT")
    except ValueError:
        raise ValueError("Quantity must be a positive number")
    if not symbol.endswith('USDT'):
        raise ValueError("Symbol must end with USDT (e.g., BTCUSDT)")
    return symbol, side, str(round(q, 3))

def place_market_order(bot, symbol, side, qty):
    """Place market order (PDF: BUY/SELL, output details/execution status)"""
    if not check_balance(bot, symbol):
        return None
    
    try:
        symbol, side, qty = validate_and_round(symbol, side, qty)
        step_size = get_step_size(bot, symbol)
        rounded_qty = str(round(float(qty) / step_size) * step_size)
        print(f"Auto-rounded qty to {rounded_qty} (step size: {step_size})")
    except ValueError as e:
        print(f"Validation Error: {e}")
        bot.logger.error(f"Market validation fail: {e}")
        return None
    
    if args.test:  # Simulate order
        print("TEST MODE: Simulating market order (no API call)...")
        simulated_order = {'orderId': 999999, 'status': 'FILLED', 'price': 60500.00}
        bot.logger.info(f"SIMULATED Market order: {simulated_order}")
        print("🎉 SIMULATED Market Order Placed Successfully!")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {rounded_qty}")
        print(f"Approx. Price: ${simulated_order['price']:,.2f}")
        print(f"Order ID: {simulated_order['orderId']}")
        print(f"Status: {simulated_order['status']}")
        return simulated_order
    
    # Real leverage set
    leverage_set = bot.safe_call(
        bot.client.futures_change_leverage,
        symbol=symbol,
        leverage=1,
        recvWindow=5000
    )
    if not leverage_set:
        print("⚠️ Leverage set failed – retry or check API perms.")
        return None
    print("Leverage set to 1x for safe trading.")
    bot.logger.info(f"Leverage set to 1x for {symbol}")
    
    # Real ticker
    ticker = bot.safe_call(bot.client.futures_symbol_ticker, symbol=symbol)
    if not ticker:
        return None
    current_price = float(ticker['price'])
    
    # Real order
    order = bot.safe_call(
        bot.client.futures_create_order,
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=rounded_qty
    )
    if order:
        print("🎉 Market Order Placed Successfully!")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Quantity: {rounded_qty}")
        print(f"Approx. Price: ${current_price:,.2f}")
        print(f"Order ID: {order['orderId']}")
        print(f"Status: {order['status']}")
        bot.logger.info(f"Market order executed: ID {order['orderId']}, Status {order['status']}, Qty {rounded_qty}")
        return order
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Market Orders Bot")
    parser.add_argument("symbol", help="Symbol e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity e.g., 0.001")
    parser.add_argument("--test", action="store_true", help="Simulate order (bypass API/balance)")
    args = parser.parse_args()
    
    bot = BasicBot()
    place_market_order(bot, args.symbol, args.side, args.quantity)

    