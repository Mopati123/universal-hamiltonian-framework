# Credentials Setup Guide
## How to Configure API Keys for Live Trading

**⚠️ IMPORTANT: This guide is for LIVE TRADING with REAL MONEY. Follow carefully!**

---

## 🎯 **Quick Start**

### **Step 1: Copy Template**
```bash
cd experiments/markets
cp .env.template .env
```

### **Step 2: Edit `.env` File**
```bash
# Use any text editor
notepad .env       # Windows
nano .env          # Linux/Mac
code .env          # VS Code
```

### **Step 3: Fill In Your Credentials**
See detailed instructions below for each API.

### **Step 4: Never Commit `.env`**
```bash
# .env is already in .gitignore
# NEVER commit it to Git!
git status  # Should NOT show .env
```

---

## 🔐 **API Credentials Guide**

### **1. MetaTrader 5 (MT5)**

**What it's for**: Forex & CFD trading, tick-level data

#### **Getting Credentials:**

**Option A: Demo Account (Free, Recommended for Testing)**
1. Download MT5: https://www.metatrader5.com/en/download
2. Install and launch
3. File → Open an Account → Create Demo Account
4. Choose any broker (e.g., "MetaQuotes-Demo")
5. Note down:
   - Account number (e.g., 12345678)
   - Password
   - Server name (e.g., "MetaQuotes-Demo")

**Option B: Real Account (Real Money)**
1. Choose a broker (Admirals, FXTM, IC Markets, etc.)
2. Sign up and verify identity
3. Fund account
4. Get login credentials from broker

#### **Add to `.env`:**
```bash
MT5_ACCOUNT=12345678
MT5_PASSWORD=YourPassword
MT5_SERVER=MetaQuotes-Demo
MT5_TERMINAL_PATH=C:/Program Files/MetaTrader 5/terminal64.exe
```

---

### **2. Deriv API**

**What it's for**: Binary options, synthetic indices, forex

#### **Getting Credentials:**

1. **Create Account**: https://deriv.com
2. **Verify Email**: Check your inbox
3. **Get API Token**:
   - Login to Deriv
   - Go to: https://app.deriv.com/account/api-token
   - Click "Create new token"
   - Name it: "Quantum Trading Bot"
   - Permissions: Select "Trading" and "Payments"
   - Click "Create"
   - **COPY YOUR TOKEN IMMEDIATELY** (shown only once!)

4. **Get App ID**:
   - It's shown on the API token page
   - Usually 4-5 digits (e.g., "12345")

#### **Add to `.env`:**
```bash
DERIV_APP_ID=12345
DERIV_API_TOKEN=your_very_long_token_string_here
```

**Demo Mode** (No registration needed):
```bash
DERIV_APP_ID=1089
DERIV_API_TOKEN=  # Leave empty for demo
```

---

### **3. Alpaca Markets**

**What it's for**: US stocks & ETFs

#### **Getting Credentials:**

1. **Sign Up**: https://alpaca.markets
2. **Choose "Paper Trading"** (Free, fake money)
3. **Verify Email**
4. **Get API Keys**:
   - Login to dashboard
   - Go to: Account → API Keys (Paper)
   - Click "Generate New Keys"
   - **COPY BOTH** Key ID and Secret Key

5. **For Live Trading** (Real Money):
   - Complete identity verification
   - Fund account
   - Use "Live Trading" API keys instead

#### **Add to `.env`:**

**Paper Trading** (Fake money, recommended):
```bash
ALPACA_API_KEY=PK...your_key_id_here
ALPACA_API_SECRET=...your_secret_key_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

**Live Trading** (REAL MONEY):
```bash
ALPACA_API_KEY=AK...your_live_key_id
ALPACA_API_SECRET=...your_live_secret_key
ALPACA_BASE_URL=https://api.alpaca.markets
```

---

### **4. TradingView**

**What it's for**: Technical indicators, chart analysis

**No credentials needed!** TradingView connector uses public API.

```bash
TRADINGVIEW_USERNAME=
TRADINGVIEW_PASSWORD=
```

---

### **5. yfinance**

**What it's for**: Historical data, options chains

**No credentials needed!** Completely free.

---

## ⚙️ **Trading System Configuration**

### **Basic Settings**

```bash
# Mode: 'simulation' (fake money) or 'live' (real money)
TRADING_MODE=simulation

# How much to trade with
TRADING_CAPITAL=10000.00

# Which symbols to trade (comma-separated)
TRADING_UNIVERSE=SPY,QQQ,IWM

# Which data sources to use
ENABLED_DATA_SOURCES=Alpaca,yfinance

# Where to send orders
PRIMARY_EXECUTION_SOURCE=Alpaca
```

---

### **Risk Management** (CRITICAL!)

```bash
# Maximum $ per position
MAX_POSITION_SIZE=5000.00

# Maximum number of open positions
MAX_POSITIONS=5

# Maximum drawdown before stop (15% = 0.15)
MAX_DRAWDOWN=0.15

# Maximum leverage
MAX_LEVERAGE=2.0
```

---

### **Safety Settings** (CRITICAL!)

```bash
# Require explicit confirmation for live trading
REQUIRE_EXPLICIT_LIVE_CONFIRMATION=true

# Dry run mode (simulate orders without executing)
DRY_RUN=false

# Logging level
LOG_LEVEL=INFO
```

---

## 🚀 **Testing Your Configuration**

### **1. Verify Configuration**
```bash
cd experiments/markets
python quantum_trading/config.py
```

**Expected output:**
```
Testing configuration loader...

✅ Loaded configuration from: .../markets/.env

TRADING SYSTEM CONFIGURATION
================================================================
Mode: SIMULATION
Capital: $10,000.00
Universe: SPY, QQQ, IWM
Max Positions: 5
Max Position Size: $5,000.00
Max Drawdown: 15.0%
Primary Execution: Alpaca
Data Sources: Alpaca, yfinance
================================================================

✅ Configuration is valid!
```

---

### **2. Test in Simulation Mode FIRST**

```bash
# Make sure mode is 'simulation'
TRADING_MODE=simulation

# Run demo
python run_quantum_trading_demo.py
```

This uses **fake money**. No risk!

---

### **3. Enable Live Trading (REAL MONEY!)**

```bash
# In .env file, change:
TRADING_MODE=live
```

```bash
# Run
python run_quantum_trading_demo.py
```

**You'll see:**
```
⚠️  WARNING: LIVE TRADING MODE ENABLED
================================================================
This will trade with REAL MONEY!
Make sure:
  1. You've tested in simulation mode first
  2. Your API credentials are correct
  3. Risk limits are properly configured
  4. You understand the risks involved

Type 'YES I UNDERSTAND' to proceed:
```

**Type exactly:** `YES I UNDERSTAND`

---

## 🔐 **Security Best Practices**

### **DO:**
- ✅ Keep `.env` file SECRET
- ✅ Use paper trading accounts first
- ✅ Start with small amounts
- ✅ Set conservative risk limits
- ✅ Enable all safety checks
- ✅ Use `DRY_RUN=true` to test without executing

### **DON'T:**
- ❌ Commit `.env` to Git
- ❌ Share your API keys
- ❌ Start with large amounts
- ❌ Disable safety checks
- ❌ Trade without testing first
- ❌ Use production keys in development

---

## 📝 **Example `.env` File**

```bash
# MT5 (Demo Account)
MT5_ACCOUNT=12345678
MT5_PASSWORD=demo_password
MT5_SERVER=MetaQuotes-Demo
MT5_TERMINAL_PATH=C:/Program Files/MetaTrader 5/terminal64.exe

# Deriv (Real credentials)
DERIV_APP_ID=54321
DERIV_API_TOKEN=abc123xyz...very_long_token

# Alpaca (Paper Trading)
ALPACA_API_KEY=PK1234567890ABCDEF
ALPACA_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Trading Configuration
TRADING_MODE=simulation
TRADING_CAPITAL=10000.00
TRADING_UNIVERSE=SPY,QQQ,IWM
ENABLED_DATA_SOURCES=Alpaca,yfinance
PRIMARY_EXECUTION_SOURCE=Alpaca

# Risk Management
MAX_POSITION_SIZE=2500.00
MAX_POSITIONS=3
MAX_DRAWDOWN=0.10
MAX_LEVERAGE=1.5

# Safety
REQUIRE_EXPLICIT_LIVE_CONFIRMATION=true
DRY_RUN=false
LOG_LEVEL=INFO
```

---

## ❓ **Troubleshooting**

### **"Configuration file not found"**
```bash
# Make sure you're in the right directory
cd experiments/markets

# Check if .env exists
ls -la .env      # Linux/Mac
dir .env         # Windows

# If not, copy template
cp .env.template .env
```

### **"Invalid credentials"**
- Double-check API keys (no typos!)
- Ensure keys are active (not revoked)
- For Alpaca: Use paper keys for paper URL
- For MT5: Ensure MT5 terminal is installed

### **"Insufficient permissions"**
- Check API token has trading permissions
- For Deriv: Recreate token with "Trading" permission
- For Alpaca: Ensure not using read-only keys

### **"Live trading not confirmed"**
- Must type **exactly**: `YES I UNDERSTAND`
- Case-sensitive
- No extra spaces

---

## 🎓 **Recommended Workflow**

### **Phase 1: Learn (Week 1)**
```bash
TRADING_MODE=simulation
TRADING_CAPITAL=10000.00
```
Run for 1 week, observe behavior

### **Phase 2: Paper Trade (Week 2-3)**
```bash
# Use real data but fake execution
PRIMARY_EXECUTION_SOURCE=Alpaca
# Use paper trading keys
```
Test with realistic data

### **Phase 3: Micro Live (Week 4)**
```bash
TRADING_MODE=live
TRADING_CAPITAL=100.00  # Start SMALL!
MAX_POSITION_SIZE=50.00
```
Real money but tiny amounts

### **Phase 4: Scale Up (Month 2+)**
```bash
# Only after consistent results
TRADING_CAPITAL=1000.00  # Still small
```
Gradually increase if profitable

---

## 📞 **Getting Help**

**Issues with credentials?**
- Check API provider's documentation
- Contact their support
- Test credentials via their web interface first

**Issues with trading system?**
- Check `trading_log.csv` for errors
- Set `LOG_LEVEL=DEBUG` for details
- Review GitHub issues

---

## ⚠️ **Final Warning**

**LIVE TRADING INVOLVES REAL FINANCIAL RISK**

- You can lose your entire capital
- Past performance ≠ future results
- Quantum trading is experimental
- No guarantees of profit
- Start with money you can afford to lose

**By entering live mode**credits, you acknowledge:
1. You understand the risks
2. You've tested thoroughly in simulation
3. You accept full responsibility
4. You won't blame the framework for losses

---

**Ready to trade? Set up your `.env` file and start with simulation mode!** 🚀

---

_For questions, see experiments/markets/README.md or GitHub issues._
