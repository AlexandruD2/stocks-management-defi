"""
Backfill historical price data - Quick 1-year history loader
Run this once to populate the database with 1 year of historical data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from database_manager import DatabaseManager
from config import ALL_TICKERS
import time


def backfill_historical_data():
    """Fetch and store 1 year of historical data for all stocks"""
    db = DatabaseManager()

    print("\n" + "="*80)
    print("BACKFILLING HISTORICAL DATA - 1 YEAR")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total stocks: {len(ALL_TICKERS)}")
    print("="*80 + "\n")

    successful = 0
    failed = 0

    for idx, ticker in enumerate(ALL_TICKERS, 1):
        try:
            print(f"[{idx}/{len(ALL_TICKERS)}] Backfilling {ticker}...", end=" ")

            # Fetch 1 year of data
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")

            if hist.empty:
                print("[NO DATA]")
                failed += 1
                continue

            # Store all historical prices
            for date, row in hist.iterrows():
                db.insert_daily_prices(
                    ticker,
                    date.date(),
                    row["Open"],
                    row["Close"],
                    row["High"],
                    row["Low"],
                    int(row["Volume"])
                )

            print(f"[OK] ({len(hist)} days)")
            successful += 1

            # Be nice to the API
            time.sleep(0.5)

        except Exception as e:
            print(f"[ERROR] {str(e)[:40]}")
            failed += 1
            continue

    print("\n" + "="*80)
    print(f"BACKFILL COMPLETE!")
    print(f"Successful: {successful}/{len(ALL_TICKERS)}")
    print(f"Failed: {failed}/{len(ALL_TICKERS)}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    print("\n[DONE] Your database is now loaded with ~250 days of historical data per stock")
    print("[DONE] Volatility and Historical tabs will now show full 60+ days of data")
    print("[DONE] You can now adjust the days slider to see longer periods\n")


if __name__ == "__main__":
    backfill_historical_data()
