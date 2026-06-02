"""
Data Collection from yfinance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from database_manager import DatabaseManager
from config import TICKERS, ALL_TICKERS, DAYS_LOOKBACK


class DataCollector:
    def __init__(self):
        self.db = DatabaseManager()

    def fetch_stock_info(self, ticker):
        """Fetch comprehensive stock information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Extract key fundamentals
            fundamentals = {
                "price": info.get("currentPrice"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": (info.get("dividendYield") or 0) * 100,
                "market_cap": info.get("marketCap"),
                "revenue": info.get("totalRevenue"),
                "net_income": info.get("netIncome"),
                "book_value": info.get("bookValue"),
                "eps": info.get("trailingEps"),
                "name": info.get("longName"),
            }

            return fundamentals
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return None

    def fetch_historical_prices(self, ticker, period="1y"):
        """Fetch historical price data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching historical prices for {ticker}: {e}")
            return None

    def fetch_quarterly_financials(self, ticker):
        """Fetch quarterly financial data"""
        try:
            stock = yf.Ticker(ticker)
            # Get earnings dates and estimates
            try:
                earnings_dates = stock.quarterly_financials
                return earnings_dates
            except:
                return None
        except Exception as e:
            print(f"Error fetching financials for {ticker}: {e}")
            return None

    def collect_all_data(self):
        """Collect data for all tickers and store in database"""
        print(f"Starting data collection for {len(ALL_TICKERS)} stocks...")

        # Initialize stocks in database
        for sector, tickers in TICKERS.items():
            for ticker in tickers:
                info = self.fetch_stock_info(ticker)
                if info:
                    self.db.insert_stock(ticker, info.get("name"), sector)
                    print(f"✓ Initialized {ticker}")

        # Fetch and store historical prices and fundamentals
        for ticker in ALL_TICKERS:
            try:
                print(f"Fetching data for {ticker}...")

                # Get current fundamentals
                info = self.fetch_stock_info(ticker)
                if info and info.get("price"):
                    self.db.insert_fundamentals(
                        ticker,
                        datetime.now().date(),
                        info.get("price"),
                        info.get("pe_ratio"),
                        info.get("dividend_yield"),
                        info.get("market_cap"),
                        info.get("revenue"),
                        info.get("net_income"),
                        info.get("book_value"),
                        info.get("eps")
                    )

                # Get historical prices
                hist = self.fetch_historical_prices(ticker, period="1y")
                if hist is not None:
                    for date, row in hist.iterrows():
                        self.db.insert_daily_prices(
                            ticker,
                            date.date(),
                            row["Open"],
                            row["Close"],
                            row["High"],
                            row["Low"],
                            int(row["Volume"])
                        )

                print(f"✓ Completed {ticker}")

            except Exception as e:
                print(f"✗ Error processing {ticker}: {e}")

        print("Data collection complete!")

    def update_daily_data(self):
        """Update only today's data (for scheduled runs)"""
        print("Updating daily data...")
        today = datetime.now().date()

        for ticker in ALL_TICKERS:
            try:
                # Update fundamentals
                info = self.fetch_stock_info(ticker)
                if info and info.get("price"):
                    self.db.insert_fundamentals(
                        ticker,
                        today,
                        info.get("price"),
                        info.get("pe_ratio"),
                        info.get("dividend_yield"),
                        info.get("market_cap"),
                        info.get("revenue"),
                        info.get("net_income"),
                        info.get("book_value"),
                        info.get("eps")
                    )

                # Update daily prices
                hist = self.fetch_historical_prices(ticker, period="5d")
                if hist is not None:
                    for date, row in hist.iterrows():
                        self.db.insert_daily_prices(
                            ticker,
                            date.date(),
                            row["Open"],
                            row["Close"],
                            row["High"],
                            row["Low"],
                            int(row["Volume"])
                        )

            except Exception as e:
                print(f"Error updating {ticker}: {e}")

        print("Daily update complete!")


if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_all_data()
