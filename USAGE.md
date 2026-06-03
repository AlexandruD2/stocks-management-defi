# Quick Start - Stock Screener Usage

## Simple Commands

### 1️⃣ Quick Market Scan (5 seconds)
```bash
python run_screener.py --quick
```
Shows top 5 stocks by score with key metrics.

**Output:**
- Ticker, Price, Score, YoY Return

---

### 2️⃣ Full Daily Report (2-3 minutes)
```bash
python run_screener.py
```
Comprehensive daily screening of all 35 stocks.

**Output:**
- Sector summaries
- Top 10 performers
- Bottom 10 performers
- Value stocks (Low PE, High Dividend)
- Growth stocks (YoY > 20%)
- CSV export with all metrics

---

### 3️⃣ Report + Buy/Sell Signals (3-4 minutes)
```bash
python run_screener.py --analyze
```
Runs screening AND generates buy/sell signals.

**Output:**
- All of #2 above
- Buy/Sell signal analysis by stock
- Signal strength ratings

---

### 4️⃣ Dashboard
```bash
streamlit run dashboard.py
```
Opens interactive web dashboard at `http://localhost:8501`

**Features:**
- Real-time signals
- Portfolio tracking
- Performance charts
- Historical data analysis

---

## Data Provided

### Daily Open/Close
```
Ticker | Date | Open | Close | High | Low | Volume | Change %
NVDA   | 2026-06-03 | 215.50 | 217.32 | 218.00 | 215.10 | 45.2M | +0.84%
```

### Year-on-Year Metrics
```
Ticker | YoY Return | 52W High | 52W Low | From High | From Low
NVDA   | +53.87%    | $220.00  | $142.00 | -1.22%    | +53.06%
```

### Fundamental Data
```
Ticker | Price | PE Ratio | Div Yield | EPS | Market Cap | Score
NVDA   | 217.32 | 72.40 | 0.05% | $3.00 | $5.35T | 60.0
```

### Stock Scoring
- **PE Ratio** — Low PE (< 20) = +10 points
- **Dividend** — High yield (> 2%) = +10 points
- **Growth** — YoY positive = +5 points
- **Earnings** — 10%+ growth = +10 points
- **Base Score** — 50 points

---

## Stock Categories

### Value Stocks
PE < 20 AND Dividend Yield > 2%
```
Screener output shows: "VALUE STOCKS"
```

### Growth Stocks  
YoY Return > 20%
```
Screener output shows: "GROWTH STOCKS"
```

### Top Performers
Sorted by YoY Return (highest)
```
Screener output shows: "TOP 10 PERFORMERS"
```

---

## Database Storage

All data is automatically saved to SQLite database:
- `database/stocks.db`
- Tables: daily_prices, fundamentals, signals, portfolio

**Access data programmatically:**
```python
from database_manager import DatabaseManager

db = DatabaseManager()

# Get today's prices
prices = db.get_daily_prices("NVDA", days=5)

# Get latest fundamentals
fund = db.get_latest_fundamentals("AAPL")

# Get recent signals
signals = db.get_latest_signals(days=7)
```

---

## CSV Reports

Each run generates a timestamped CSV:
```
stock_report_20260603_143022.csv
```

Contains:
- ticker, date, open, close, change_percent
- yoy_return_percent, 52w_high, 52w_low
- pe_ratio, dividend_yield, eps, score

---

## Sector Coverage

1. **Artificial Intelligence** — NVDA, TSLA, PLTR, AI, UPST
2. **Healthcare** — JNJ, UNH, PFE, ABBV, LLY
3. **Information Technology** — AAPL, MSFT, GOOGL, META, IBM
4. **Communication Services** — DIS, VZ, T, CMCSA, FOX
5. **Industrials** — BA, CAT, GE, HON, RTX
6. **Energy** — XOM, CVX, COP, MPC, EOG
7. **Utilities** — NEE, DUK, SO, AEP, EXC

**Total: 35 stocks**

---

## Scheduling (Optional)

### Windows - Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 4:00 PM (after market close)
4. Action: Run `python run_screener.py`
5. Working directory: `C:\Users\Alex\OneDrive\Desktop\Stocks_Management_Defi`

### Linux/Mac - Crontab
```bash
# Run daily at 4:00 PM
0 16 * * * cd ~/Stocks_Management_Defi && python run_screener.py >> screener.log 2>&1
```

---

## Output Example

```
================================================================================
DAILY STOCK SCREENER REPORT - 2026-06-03 14:30:22
================================================================================

SECTOR SUMMARY
----------------

Artificial Intelligence:
  Stocks: 5
  Avg PE: 85.23
  Avg Dividend: 0.02%
  Avg YoY Return: +5.34%

Healthcare:
  Stocks: 5
  Avg PE: 28.45
  Avg Dividend: 1.52%
  Avg YoY Return: +8.12%

...

TOP 10 PERFORMERS (by YoY Return)
NVDA     | Price: $ 217.32 | Daily: +0.84% | YoY: +53.87% | PE: 72.40 | Div: 0.05% | Score:  60.0
TSLA     | Price: $ 422.47 | Daily: +1.23% | YoY: +22.72% | PE: 65.30 | Div: 0.00% | Score:  40.0
...

VALUE STOCKS (PE < 20 & Dividend > 2%)
JNJ      | Price: $ 156.20 | PE:  18.50 | Div: 3.45% | Score:  70.0
PFE      | Price: $  28.15 | PE:  15.20 | Div: 5.80% | Score:  80.0
...

Report saved to: stock_report_20260603_143022.csv
================================================================================
```

---

## Troubleshooting

**No data returned?**
- Check internet connection
- yfinance API might be rate-limited
- Wait a few minutes and retry

**Database errors?**
- Delete `database/stocks.db` to reset
- Next run will recreate it

**Need real-time updates?**
- Run `python run_screener.py` after market close daily
- Or use Task Scheduler / cron for automation

---

## What's Next?

1. **Review Reports** — Check CSV exports for trends
2. **Add Portfolio** — Update with your holdings in dashboard
3. **Set Alerts** — Watch for BUY/SELL signals
4. **Backtest Strategies** — Use historical data for testing

---

Last Updated: June 3, 2026
