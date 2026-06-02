# Stocks Management & Portfolio Tracking System

A comprehensive stock portfolio management system with real-time monitoring, AI-driven buy/sell signals, and interactive Streamlit dashboard.

## 🎯 Features

- **Real-time Stock Monitoring** — Track 35+ stocks across 7 sectors
- **Buy/Sell Signals** — AI-generated signals based on:
  - Moving Average Analysis (Golden Cross / Death Cross)
  - Dividend Yield Changes
  - Earnings Surprises
  - Valuation Metrics (PE Ratio)
- **Portfolio Tracking** — Monitor holdings, cost basis, and returns
- **Performance Analytics** — Year-on-year profits, quarterly metrics, statistical analysis
- **Interactive Dashboard** — Real-time Streamlit interface with charts and insights
- **SQLite Database** — Persistent storage of all historical data

## 📊 Sectors Covered

1. **Artificial Intelligence** — NVDA, TSLA, PLTR, AI, UPST
2. **Healthcare** — JNJ, UNH, PFE, ABBV, LLY
3. **Information Technology** — AAPL, MSFT, GOOGL, META, IBM
4. **Communication Services** — DIS, VZ, T, CMCSA, FOX
5. **Industrials** — BA, CAT, GE, HON, RTX
6. **Energy** — XOM, CVX, COP, MPC, EOG
7. **Utilities** — NEE, DUK, SO, AEP, EXC

## 🏗️ Project Structure

```
Stocks_Management_Defi/
├── config.py                 # Configuration & ticker list
├── database_manager.py       # SQLite database operations
├── data_collection.py        # yfinance data fetching
├── analysis.py              # Signal generation & analysis
├── main.py                  # Orchestration script
├── dashboard.py             # Streamlit app
├── database/                # SQLite database files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Installation

```bash
cd Stocks_Management_Defi
pip install -r requirements.txt
```

### Run Full Pipeline (Initial Setup)

```bash
python main.py --mode full
```

This will:
1. Fetch all historical data from yfinance (1 year)
2. Store in SQLite database
3. Generate buy/sell signals for all stocks

### Daily Update

```bash
python main.py --mode daily
```

This will:
1. Update prices for the current day
2. Refresh fundamentals
3. Regenerate signals

### Launch Dashboard

```bash
streamlit run dashboard.py
```

Opens the interactive dashboard at `http://localhost:8501`

## 📈 Dashboard Tabs

### 1. **Signals** 📈
- Recent buy/sell signals (last 7 days)
- Signal strength distribution
- Breakdown by signal type (BUY/SELL)

### 2. **Portfolio** 💼
- Current holdings and shares owned
- Cost basis and current value
- Gain/loss tracking with percentages
- Portfolio allocation pie chart

### 3. **Performance** 📊
- Average PE ratio and dividend yields
- Price comparisons across stocks
- Scatter plot: PE vs Dividend Yield
- Bar chart: PE ratio rankings

### 4. **Fundamentals** 🔍
- Individual stock analysis
- Key metrics: Price, PE, Dividend, EPS, Market Cap
- 90-day price history chart
- Candlestick chart analysis

### 5. **Historical Data** 📅
- Extended historical price analysis
- Candlestick charts (customizable days)
- Trading volume analysis
- Data export table

## 🎛️ Signal Generation Logic

### Moving Averages
- **Golden Cross** (SMA20 > SMA50 > SMA200) = **BUY**
- **Death Cross** (SMA20 < SMA50 < SMA200) = **SELL**
- Price above SMA20 = Bullish
- Price below SMA20 = Bearish

### Dividend Yield
- High yield (>2.5%) + increasing trend = **BUY**
- Decreasing trend = **SELL**
- Threshold: 0.5% change to trigger alert

### Earnings Quality
- 3+ consecutive positive surprises = **BUY**
- 2+ negative surprises = **SELL**
- Threshold: ±5% surprise

### Valuation
- PE < 15 = **BUY** (undervalued)
- PE > 25 = **SELL** (overvalued)

## 📊 Database Schema

### Tables

**stocks** — Master list of stocks
- ticker, name, sector, last_updated

**daily_prices** — OHLCV data
- ticker, date, open, close, high, low, volume

**fundamentals** — Periodic snapshots
- ticker, date, price, pe_ratio, dividend_yield, market_cap, revenue, net_income, eps

**earnings** — Earnings surprises
- ticker, quarter, eps_estimate, eps_actual, surprise_percent

**portfolio** — Holdings tracking
- ticker, shares_owned, average_cost, date_added

**signals** — Generated buy/sell signals
- ticker, signal_type, signal_reason, strength, date

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Add/remove tickers
TICKERS = {
    "Sector": ["TICKER1", "TICKER2", ...],
}

# Signal thresholds
SIGNAL_THRESHOLDS = {
    "dividend_yield_change": 0.5,  # % change
    "price_sma_20": 20,            # SMA period
    "price_sma_50": 50,            # SMA period
}

# Database path
DB_PATH = "database/stocks.db"

# Dashboard settings
DAYS_LOOKBACK = 252  # 1 year
DASHBOARD_REFRESH_INTERVAL = 3600  # 1 hour
```

## 📝 Usage Examples

### Add Stock to Portfolio

```python
from database_manager import DatabaseManager

db = DatabaseManager()
db.update_portfolio("AAPL", shares_owned=10, average_cost=150.25)
```

### Get Latest Signals

```python
signals = db.get_latest_signals(days=7)
for ticker, signal_type, reason, strength, date in signals:
    print(f"{ticker}: {signal_type} ({reason})")
```

### Get Stock Fundamentals

```python
fundamentals = db.get_latest_fundamentals("MSFT")
price, pe_ratio, dividend_yield = fundamentals[2], fundamentals[3], fundamentals[4]
```

## 🎯 Key Metrics

- **Total Stocks Tracked** — 35 stocks
- **Sectors** — 7 major sectors
- **Signal Types** — 8 different reasons (moving averages, dividends, earnings, valuation)
- **Data Retention** — 252 days (1 year) minimum
- **Update Frequency** — Daily (configurable)

## 🔄 Scheduling (Optional)

For automated daily updates, use Windows Task Scheduler or cron:

```bash
# Windows (Task Scheduler)
python C:\path\to\Stocks_Management_Defi\main.py --mode daily

# Linux/Mac (crontab)
0 16 * * 1-5 cd ~/Stocks_Management_Defi && python main.py --mode daily
```

## 📚 Dependencies

- **yfinance** — Stock data from Yahoo Finance
- **pandas** — Data manipulation
- **numpy** — Numerical computations
- **streamlit** — Interactive dashboard
- **plotly** — Interactive charts
- **sqlite3** — Database (built-in)

## ⚠️ Disclaimer

This system is for educational and informational purposes only. It does not constitute financial advice. Always conduct your own research and consult a financial advisor before making investment decisions.

## 🤝 Contributing

Feel free to extend the system with:
- Additional signal types (RSI, MACD, Bollinger Bands)
- ML-based predictions
- Backtesting module
- Email/SMS alerts
- Portfolio optimization algorithms

## 📧 Contact

For questions or suggestions: alexandrugabos1@gmail.com

---

**Last Updated:** June 2, 2026
