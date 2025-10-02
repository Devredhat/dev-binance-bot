# Binance Futures Trading Bot - Report

## Student Submission
**Name:** Dev Suthar  
**Date:** 02/10/2025  
**Project:** Simplified Trading Bot

## Project Overview
I developed a CLI-based trading bot for **Binance USDT-M Futures Testnet** that supports the following features:
- ✅ **Market Orders**
- ✅ **Limit Orders**  
- ✅ **OCO Orders** (Bonus)
- ✅ **Input Validation & Error Handling**
- ✅ **Comprehensive Logging**
- ✅ **Test Mode** for Safe Testing

---

## 🚀 Quick Setup

### Option A: GUI Interface

1. **Install Dependencies**  
   Run the following command to install the necessary dependencies:
   ```bash
   pip install python-binance python-dotenv flask flask-cors
   ```

2. **Setup API Keys**  
   Create a `.env` file and add your Binance API credentials:
   ```bash
   echo "API_KEY=f9e7faab0b4873c0908b5c42b24fabe81534fc1400b34d5c1b6bade0b1db0f87" > .env
   echo "API_SECRET=c51f76b6c0fe156d03dfdfd34dfde2df18c2f90325ac73a76109d1c49b8fdf2c" >> .env
   ```

3. **Run the Bot**  
   Clone the repository and run the Flask app:
   ```bash
   git clone https://github.com/Devredhat/dev-binance-bot.git
   cd dev-binance-bot/src/frontend
   python app.py
   ```
   After that, open the web interface in your browser:
   ```
   http://localhost:5000
   ```

### Option B: CLI Interface

- **Market Orders**
   ```bash
   python src/market_orders.py BTCUSDT BUY 0.001 --test
   ```

- **Limit Orders**
   ```bash
   python src/limit_orders.py BTCUSDT BUY 0.001 50000 --test
   ```

- **OCO Orders (Bonus)**
   ```bash
   python src/advanced/oco.py BTCUSDT BUY 0.001 52000 48000 47500 --test
   ```

---

## 📁 Project Structure

```plaintext
binance-bot/
├── src/                          # Core trading engine
│   ├── bot_base.py               # Base class with API client
│   ├── market_orders.py          # Market order implementation
│   ├── limit_orders.py           # Limit order implementation
│   └── advanced/
│       └── oco.py                # OCO order implementation
├── frontend/                     # Web interface
│   ├── app.py                    # Flask server
│   ├── index.html                # Main interface
│   ├── style.css                 # Professional styling
│   └── script.js                 # Interactive functionality
├── bot.log                       # Auto-generated logs
├── .env                          # API credentials (create this)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## ⚡ Features

- ✅ **Market & Limit Orders**
- ✅ **OCO Orders** (Take-profit + Stop-loss)
- ✅ **Web Interface + CLI**
- ✅ **Test Mode** (`--test` flag)
- ✅ **Real-time Logging**

---

## 🛠️ Usage Tips

- Use the `--test` flag to perform **safe testing** without executing real trades.
- Check `bot.log` for detailed logs and debugging information.
- **Web UI:**  
  After opening the Flask app (`http://localhost:5000`), click the **"Connect"** button to connect your Binance account and place orders.
- You can obtain **Binance Testnet API keys** from [Binance Futures Testnet](https://testnet.binancefuture.com/).
