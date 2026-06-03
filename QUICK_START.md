# Stock Management System - Quick Start Guide

## What You Have

A complete stocks portfolio management system with:
- ✓ Data collection from yfinance (35 stocks, 7 sectors)
- ✓ SQLite database storage (persistent)
- ✓ Daily stock screener with reports
- ✓ Buy/Sell signal generation
- ✓ Interactive Streamlit dashboard
- ✓ CSV exports for analysis

---

## 3 Main Commands

### 1. Quick Scan (30 seconds)
```bash
python run_screener.py --quick
```
Shows top stocks by score. Good for quick market overview.

### 2. Full Daily Report (3 minutes)
```bash
python run_screener.py
```
Complete screening of all 35 stocks with:
- Sector summaries
- Top/bottom performers
- Value stocks (low PE, high dividend)
- Growth stocks (YoY > 20%)
- CSV export with all metrics

### 3. Dashboard (Real-time)
```bash
streamlit run dashboard.py
```
Opens web dashboard with:
- Buy/Sell signals
- Portfolio tracking
- Performance charts
- Historical analysis

---

## Data Tracked

### Daily Metrics
| Metric | Example | Purpose |
|--------|---------|---------|
| Open/Close | $216.96 | Daily price movement |
| Change % | -2.63% | Daily performance |
| Volume | 45.2M | Trading activity |

### Year-on-Year Metrics
| Metric | Example | Purpose |
|--------|---------|---------|
| YoY Return | +53.71% | Annual performance |
| 52W High | $236.54 | Price ceiling |
| 52W Low | $137.92 | Price floor |

### Fundamental Metrics
| Metric | Example | Purpose |
|--------|---------|---------|
| PE Ratio | 33.24 | Valuation |
| Dividend Yield | 0.05% | Income |
| Market Cap | $5.35T | Size |
| EPS | $6.53 | Earnings per share |

### Signals
| Type | Reason | Strength |
|------|--------|----------|
| BUY | Moving average golden cross | 60-100 |
| SELL | High PE valuation | 50-100 |
| BUY | Dividend yield increase | 70+ |

---

## Stock Screener Output

```
================================================================================
DAILY STOCK SCREENER REPORT - 2026-06-03 16:54:10
================================================================================

SECTOR SUMMARY
- Artificial Intelligence (5 stocks): Avg PE 164, YoY -2.87%
- Healthcare (5 stocks): Avg PE 44, YoY +32.56%
- Technology (5 stocks): Avg PE 28, YoY +35.81%
- Energy (5 stocks): Avg PE 22, YoY +44.96%
- [... etc]

TOP 10 PERFORMERS (by YoY Return)
CAT      | $921.76 | Daily: +1.31% | YoY: +166.67% | PE: 45.84 | Score: 60.0
GOOGL    | $362.11 | Daily: +0.07% | YoY: +118.66% | PE: 27.64 | Score: 70.0
[... 8 more]

VALUE STOCKS (PE < 20 & Dividend > 2%)
PFE      | $25.56  | PE: 19.52 | Dividend: 6.73% | Score: 70.0
COP      | $117.30 | PE: 19.88 | Dividend: 2.87% | Score: 70.0
[... more]

GROWTH STOCKS (YoY > 20%)
NVDA     | +53.71% | CAT | +166.67% | GOOGL | +118.66%
[... more]

Report saved to: stock_report_20260603_165442.csv
```

---

## CSV Report Example

```csv
ticker,date,open,close,change_percent,yoy_return_percent,52w_high,52w_low,pe_ratio,dividend_yield,eps,score
NVDA,2026-06-03,221.68,216.96,-2.63,53.71,236.54,137.92,33.24,0.05,6.53,60
TSLA,2026-06-03,418.70,423.09,-0.15,22.89,498.83,273.21,384.69,0.0,1.1,40
JNJ,2026-06-03,222.45,224.64,0.79,49.11,250.27,145.41,26.03,2.4,8.63,60
```

Open with Excel for easy analysis.

---

## Database Access

All data is saved to `database/stocks.db` (SQLite)

Access via Python:
```python
from database_manager import DatabaseManager

db = DatabaseManager()

# Get today's prices for NVDA (last 5 days)
prices = db.get_daily_prices("NVDA", days=5)

# Get latest fundamentals
fund = db.get_latest_fundamentals("AAPL")

# Get recent buy/sell signals
signals = db.get_latest_signals(days=7)

# Get portfolio holdings
portfolio = db.get_portfolio()
```

---

## Stock Coverage

**35 stocks across 7 sectors:**

| Sector | Stocks | Focus |
|--------|--------|-------|
| AI | NVDA, TSLA, PLTR, AI, UPST | Growth, Innovation |
| Healthcare | JNJ, UNH, PFE, ABBV, LLY | Dividends, Stability |
| Technology | AAPL, MSFT, GOOGL, META, IBM | Growth, Blue chip |
| Communication | DIS, VZ, T, CMCSA, FOX | Dividends, Streaming |
| Industrials | BA, CAT, GE, HON, RTX | Cyclical, Earnings |
| Energy | XOM, CVX, COP, MPC, EOG | Dividends, Oil/Gas |
| Utilities | NEE, DUK, SO, AEP, EXC | Stable, Dividends |

---

## Stock Scoring System

**50-point base score. Adjust for:**
- PE Ratio < 20: +10 points
- Dividend Yield > 2%: +10 points
- YoY Return > 0%: +5 points
- Earnings Growth > 10%: +10 points

**Score ranges:**
- 70-100: Strong buy signal
- 50-70: Neutral/hold
- 0-50: Caution/sell signal

---

## Setup (One time)

```bash
cd C:\Users\Alex\OneDrive\Desktop\Stocks_Management_Defi

# Install dependencies
pip install -r requirements.txt

# Run first screening (creates database)
python run_screener.py

# All done!
```

---

## Regular Usage

**Daily (after market close):**
```bash
python run_screener.py
```
Saves CSV with latest data.

**Weekly (review trends):**
```bash
python run_screener.py --analyze
```
Includes buy/sell signals.

**Anytime (view dashboard):**
```bash
streamlit run dashboard.py
```
Interactive web interface.

---

## Automate (Optional)

**Windows Task Scheduler:**
1. Task name: "Daily Stock Screening"
2. Trigger: 4:00 PM daily (after market)
3. Action: `python C:\path\to\run_screener.py`
4. Working directory: `C:\Users\Alex\OneDrive\Desktop\Stocks_Management_Defi`

**Linux/Mac cron:**
```bash
0 16 * * 1-5 cd ~/Stocks_Management_Defi && python run_screener.py >> screener.log 2>&1
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `run_screener.py` | Main entry point - run this! |
| `screener.py` | Stock screener logic |
| `analysis.py` | Buy/sell signal generation |
| `dashboard.py` | Streamlit web dashboard |
| `database_manager.py` | SQLite database operations |
| `data_collection.py` | yfinance data fetching |
| `config.py` | Tickers and thresholds |
| `database/stocks.db` | SQLite database (created automatically) |
| `stock_report_*.csv` | Daily CSV exports |

---

## Next Steps

1. **Run first screening:**
   ```bash
   python run_screener.py
   ```

2. **Review CSV report:**
   Open `stock_report_YYYYMMDD_HHMMSS.csv` in Excel

3. **Launch dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

4. **Add portfolio holdings:**
   Use dashboard → Portfolio tab

5. **Monitor signals:**
   Check dashboard → Signals tab daily

---

## Troubleshooting

**No data?**
- Check internet connection
- yfinance might be rate-limited (wait 5 minutes)

**Database error?**
- Delete `database/stocks.db`
- Next run creates new database

**Encoding errors?**
- System uses ASCII-safe characters (no Unicode)

**Slow performance?**
- First run takes 2-3 minutes (fetching 35 stocks)
- Subsequent runs are faster

---

## Questions?

Check USAGE.md for detailed command reference.

Check README.md for architecture details.

---

**Last Updated:** June 3, 2026
**Project Status:** Production Ready ✓
