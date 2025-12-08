# API Setup Guide
## Multi-Source Market Data Collection

This guide walks you through setting up API access for all data sources.

---

## 📋 Overview

You'll need accounts for:
- **MT5** (MetaTrader 5) - Raw tick data
- **Deriv** - WebSocket tick streaming
- **TradingView** - Technical indicators (no API key needed)
- **Alpaca** - Real-time quotes (free tier available)
- **yfinance** - Options data (no API key needed)

**Note**: TradingView and yfinance work without authentication. MT5, Deriv, and Alpaca require accounts.

---

## 🔧 Setup Instructions

### 1. MetaTrader 5 (MT5)

**What it provides**: Raw tick data, OHLCV bars, symbol information

#### Steps:
1. **Download MT5 terminal**:
   - Windows: https://www.metatrader5.com/en/download
   - Install the desktop application

2. **Open demo account** (free):
   - Launch MT5
   - File → Open an Account → Create demo account
   - Choose any broker (e.g., "MetaQuotes-Demo")
   - Note your credentials: Account number, Password, Server

3. **Install Python library**:
   ```bash
   pip install MetaTrader5
   ```

4. **Test connection**:
   ```python
   import MetaTrader5 as mt5
   
   # Connect
   mt5.initialize()
   print(mt5.account_info())
   mt5.shutdown()
   ```

#### Credentials needed:
- Account number (integer)
- Password (string)
- Server name (string)

**Note**: For market data only, MT5 can connect without login. Demo accounts are free and unlimited.

---

### 2. Deriv API

**What it provides**: Real-time tick streaming, historical ticks, candles

#### Steps:
1. **Create account**:
   - Go to: https://deriv.com
   - Click "Sign up" (free)
   - Verify email

2. **Get API token**:
   - Login to Deriv
   - Go to: https://app.deriv.com/account/api-token
   - Create new token
   - Copy the `app_id`

3. **Install Python library**:
   ```bash
   pip install websockets
   ```

4. **Test connection**:
   ```python
   from data_sources.deriv_connector import DerivDataCollector
   
   collector = DerivDataCollector(app_id="YOUR_APP_ID")
   data = collector.get_historical_ticks("R_100", count=100)
   print(data.head())
   ```

#### Credentials needed:
- App ID (string) - get from API token page

**Note**: There's a public demo app_id (`1089`) that works without registration, but has rate limits.

---

### 3. TradingView

**What it provides**: Technical indicators, multi-timeframe analysis

#### Steps:
1. **Install Python library**:
   ```bash
   pip install tradingview-ta
   ```

2. **Test** (no credentials needed):
   ```python
   from data_sources.tradingview_connector import TradingViewDataCollector
   
   collector = TradingViewDataCollector()
   analysis = collector.get_analysis("SPY")
   print(analysis)
   ```

#### Credentials needed:
- None! TradingView connector uses public API

---

### 4. Alpaca Markets

**What it provides**: Real-time quotes, bars, trades

#### Steps:
1. **Create account**:
   - Go to: https://alpaca.markets
   - Click "Sign Up" → Choose "Paper Trading" (free)
   - Verify email

2. **Get API keys**:
   - Login to dashboard
   - Go to: Account → API Keys (Paper)
   - Generate new keys
   - Copy:  Key ID, Secret Key

3. **Install Python library**:
   ```bash
   pip install alpaca-py alpaca-trade-api
   ```

4. **Test connection**:
   ```python
   from data_sources.alpaca_connector import AlpacaDataCollector
   
   collector = AlpacaDataCollector(
       api_key="YOUR_KEY_ID",
       api_secret="YOUR_SECRET_KEY"
   )
   
   bars = collector.get_bars("SPY", limit=10)
   print(bars)
   ```

#### Credentials needed:
- API Key ID (string)
- API Secret Key (string)

**Note**: Paper trading account is completely free, no credit card needed!

---

### 5. yfinance

**What it provides**: Historical data, options chains

#### Steps:
1. **Install Python library**:
   ```bash
   pip install yfinance
   ```

2. **Test** (no credentials needed):
   ```python
   import yfinance as yf
   
   spy = yf.Ticker("SPY")
   hist = spy.history(period="1d")
   print(hist)
   ```

#### Credentials needed:
- None! yfinance is completely free

---

## 🔐 Storing Credentials Securely

**DO NOT hardcode credentials in scripts!**

### Recommended: Use environment variables

1. **Create `.env` file** (in project root):
   ```bash
   # .env file
   
   # MT5
   MT5_ACCOUNT=12345678
   MT5_PASSWORD=your_password
   MT5_SERVER=MetaQuotes-Demo
   
   # Deriv
   DERIV_APP_ID=your_app_id
   
   # Alpaca
   ALPACA_API_KEY=your_key_id
   ALPACA_API_SECRET=your_secret
   ```

2. **Add to `.gitignore`**:
   ```bash
   echo ".env" >> .gitignore
   ```

3. **Load in Python**:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   
   mt5_account = int(os.getenv('MT5_ACCOUNT'))
   mt5_password = os.getenv('MT5_PASSWORD')
   mt5_server = os.getenv('MT5_SERVER')
   
   deriv_app_id = os.getenv('DERIV_APP_ID')
   
   alpaca_key = os.getenv('ALPACA_API_KEY')
   alpaca_secret = os.getenv('ALPACA_API_SECRET')
   ```

4. **Install python-dotenv**:
   ```bash
   pip install python-dotenv
   ```

---

## ✅ Quick Start Checklist

**Free tier (no credit card needed)**:
- [ ] Install MT5 terminal, create demo account
- [ ] Sign up for Deriv account, get app_id
- [ ] Sign up for Alpaca paper trading, get API keys
- [ ] Install TradingView library (no signup needed)
- [ ] Install yfinance (no signup needed)
- [ ] Create `.env` file with credentials
- [ ] Add `.env` to `.gitignore`
- [ ] Install all Python packages: `pip install -r requirements.txt`

**Estimated setup time**: 20-30 minutes

---

## 🧪 Testing Your Setup

Run the test script to verify all connections:

```bash
cd experiments/markets
python test_all_connectors.py
```

This will test each API and report which ones are working.

---

## ❓ Troubleshooting

### MT5 connection failed
- Ensure MT5 terminal is installed
- Try connecting without login (works for quotes)
- Check firewall isn't blocking MT5

### Deriv WebSocket timeout
- Check internet connection
- Try with demo app_id: `1089`
- Verify app_id is correct

### Alpaca authentication error
- Verify you're using Paper Trading keys (not Live)
- Check for typos in API key/secret
- Ensure no extra spaces in credentials

### TradingView no data
- Some symbols may not be available
- Try different exchange (AMEX, NYSE, NASDAQ)
- Check symbol name is correct

---

## 📚 Additional Resources

- **MT5 Python docs**: https://www.mql5.com/en/docs/python_metatrader5
- **Deriv API docs**: https://api.deriv.com
- **Alpaca docs**: https://alpaca.markets/docs/
- **TradingView TA**: https://github.com/brian-the-dev/python-tradingview-ta

---

**Next**: Once setup is complete, proceed to data collection scripts!
