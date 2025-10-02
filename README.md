# Binance Futures Trading Bot - Report

## Student Submission
**Name:** Dev Suthar
**Date:** 02/10/2025
**Project:** Simplified Trading Bot

## Project Overview
I developed a CLI-based trading bot for Binance USDT-M Futures Testnet that supports:
- ✅ Market Orders
- ✅ Limit Orders  
- ✅ OCO Orders (Bonus)
- ✅ Input Validation & Error Handling
- ✅ Comprehensive Logging
- ✅ Test Mode for Safe Testing

🚀 Quick Setup 

Option A : GUI Interface

1. Install Dependencies :-
pip install python-binance python-dotenv flask flask-cors

2. Setup API Keys :-
echo "API_KEY=f9e7faab0b4873c0908b5c42b24fabe81534fc1400b34d5c1b6bade0b1db0f87" > .env
echo "API_SECRET=c51f76b6c0fe156d03dfdfd34dfde2df18c2f90325ac73a76109d1c49b8fdf2c" >> .env

3. Run the Bot :-
cd src /
cd frontend /
python app.py

Then open: http://localhost:5000

Option B: CLI Interface

# Market Orders
python src/market_orders.py BTCUSDT BUY 0.001 --test

# Limit Orders
python src/limit_orders.py BTCUSDT BUY 0.001 50000 --test

# OCO Orders (Bonus)
python src/advanced/oco.py BTCUSDT BUY 0.001 52000 48000 47500 --test

📁 Project Structure :-

binance-bot/
├── src/                          # Core trading engine
│   ├── bot_base.py              # Base class with API client
│   ├── market_orders.py         # Market order implementation
│   ├── limit_orders.py          # Limit order implementation
│   └── advanced/
│       └── oco.py               # OCO order implementation
├── frontend/                    # Web interface
│   ├── app.py                  # Flask server
│   ├── index.html              # Main interface
│   ├── style.css               # Professional styling
│   └── script.js               # Interactive functionality
├── bot.log                     # Auto-generated logs
├── .env                        # API credentials (create this)
├── requirements.txt            # Python dependencies
└── README.md                   # This file

⚡ Features :-

✅ Market & Limit Orders
✅ OCO Orders (Take-profit + Stop-loss)
✅ Web Interface + CLI
✅ Test Mode (--test flag)
✅ Real-time Logging

🛠️ Usage Tips
Use --test flag for safe testing
Check bot.log for detailed logs
Web UI: Click "Connect" then place orders
Get Binance Testnet API keys from: https://testnet.binancefuture.com/
