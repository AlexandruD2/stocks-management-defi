"""
Simplified Stock Screener - Daily Opens/Closes, YoY Metrics, Quarterly Data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from database_manager import DatabaseManager
from config import ALL_TICKERS, TICKERS
import json


class StockScreener:
    def __init__(self):
        self.db = DatabaseManager()

    def get_daily_prices(self, ticker):
        """Get today's and previous day's prices"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")

            if len(hist) < 2:
                return None

            today = hist.iloc[-1]
            yesterday = hist.iloc[-2]

            return {
                "ticker": ticker,
                "date": hist.index[-1].date(),
                "open": today["Open"],
                "close": today["Close"],
                "high": today["High"],
                "low": today["Low"],
                "volume": int(today["Volume"]),
                "prev_close": yesterday["Close"],
                "change": today["Close"] - yesterday["Close"],
                "change_percent": ((today["Close"] - yesterday["Close"]) / yesterday["Close"] * 100) if yesterday["Close"] != 0 else 0
            }
        except Exception as e:
            print(f"Error fetching daily prices for {ticker}: {e}")
            return None

    def get_yoy_metrics(self, ticker):
        """Get year-on-year performance metrics"""
        try:
            stock = yf.Ticker(ticker)

            # Get 1-year historical data
            hist = stock.history(period="1y")

            if len(hist) < 2:
                return None

            price_now = hist.iloc[-1]["Close"]
            price_year_ago = hist.iloc[0]["Close"]
            yoy_return = ((price_now - price_year_ago) / price_year_ago * 100) if price_year_ago != 0 else 0

            # Get 52-week high/low
            week_52_high = hist["High"].max()
            week_52_low = hist["Low"].min()

            return {
                "ticker": ticker,
                "yoy_return_percent": yoy_return,
                "52w_high": week_52_high,
                "52w_low": week_52_low,
                "current_price": price_now,
                "price_from_52w_high": ((price_now - week_52_high) / week_52_high * 100) if week_52_high != 0 else 0,
                "price_from_52w_low": ((price_now - week_52_low) / week_52_low * 100) if week_52_low != 0 else 0
            }
        except Exception as e:
            print(f"Error fetching YoY metrics for {ticker}: {e}")
            return None

    def get_fundamentals(self, ticker):
        """Get key fundamental metrics"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker,
                "price": info.get("currentPrice"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": (info.get("dividendYield") or 0) * 100,
                "eps": info.get("trailingEps"),
                "revenue": info.get("totalRevenue"),
                "revenue_growth": info.get("revenueGrowth"),
                "earnings_growth": info.get("earningsGrowth"),
                "profit_margin": (info.get("profitMargins") or 0) * 100,
                "market_cap": info.get("marketCap"),
                "book_value": info.get("bookValue")
            }
        except Exception as e:
            print(f"Error fetching fundamentals for {ticker}: {e}")
            return None

    def score_stock(self, ticker_data):
        """Score stock based on simple criteria"""
        if not ticker_data:
            return 0

        score = 50  # Base score

        # PE Ratio (lower is better)
        pe = ticker_data.get("pe_ratio")
        if pe and pe < 20:
            score += 10
        elif pe and pe > 30:
            score -= 10

        # Dividend Yield (higher is better)
        div = ticker_data.get("dividend_yield")
        if div and div > 2:
            score += 10

        # YoY Return (positive is better)
        yoy = ticker_data.get("yoy_return_percent")
        if yoy and yoy > 0:
            score += 5
        elif yoy and yoy < -20:
            score -= 10

        # Earnings Growth
        eg = ticker_data.get("earnings_growth")
        if eg and eg > 0.1:  # 10% growth
            score += 10

        return max(0, min(100, score))

    def generate_daily_report(self):
        """Generate comprehensive daily screener report"""
        print("\n" + "="*80)
        print(f"DAILY STOCK SCREENER REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        all_data = []

        # Initialize stocks in database (with sector)
        for sector, tickers in TICKERS.items():
            for ticker in tickers:
                self.db.insert_stock(ticker, ticker, sector)

        for ticker in ALL_TICKERS:
            print(f"Screening {ticker}...", end=" ")

            # Get all data points
            daily = self.get_daily_prices(ticker)
            yoy = self.get_yoy_metrics(ticker)
            fundamentals = self.get_fundamentals(ticker)

            if daily and yoy and fundamentals:
                # Combine data
                ticker_data = {**daily, **yoy, **fundamentals}
                ticker_data["score"] = self.score_stock(fundamentals)

                all_data.append(ticker_data)

                # Save to database
                self.db.insert_daily_prices(
                    ticker, daily["date"],
                    daily["open"], daily["close"],
                    daily["high"], daily["low"],
                    daily["volume"]
                )

                self.db.insert_fundamentals(
                    ticker, daily["date"],
                    fundamentals.get("price"),
                    fundamentals.get("pe_ratio"),
                    fundamentals.get("dividend_yield"),
                    fundamentals.get("market_cap"),
                    fundamentals.get("revenue"),
                    fundamentals.get("revenue") * (fundamentals.get("profit_margin", 0) / 100) if fundamentals.get("revenue") else None,
                    fundamentals.get("book_value"),
                    fundamentals.get("eps")
                )

                print("[OK]")
            else:
                print("[SKIP]")

        if not all_data:
            print("\nNo data retrieved. Please check your internet connection.")
            return

        # Create DataFrame
        df = pd.DataFrame(all_data)

        # Display summary by sector
        print("\n" + "-"*80)
        print("SECTOR SUMMARY")
        print("-"*80)

        for sector, tickers in TICKERS.items():
            sector_data = df[df["ticker"].isin(tickers)]
            if not sector_data.empty:
                avg_pe = sector_data["pe_ratio"].mean()
                avg_div = sector_data["dividend_yield"].mean()
                avg_yoy = sector_data["yoy_return_percent"].mean()

                print(f"\n{sector}:")
                print(f"  Stocks: {len(sector_data)}")
                print(f"  Avg PE: {avg_pe:.2f}" if not pd.isna(avg_pe) else "  Avg PE: N/A")
                print(f"  Avg Dividend: {avg_div:.2f}%" if not pd.isna(avg_div) else "  Avg Dividend: N/A")
                print(f"  Avg YoY Return: {avg_yoy:.2f}%" if not pd.isna(avg_yoy) else "  Avg YoY Return: N/A")

        # Top performers
        print("\n" + "-"*80)
        print("TOP 10 PERFORMERS (by YoY Return)")
        print("-"*80)

        top_performers = df.nlargest(10, "yoy_return_percent")[
            ["ticker", "close", "change_percent", "yoy_return_percent", "pe_ratio", "dividend_yield", "score"]
        ]

        for idx, row in top_performers.iterrows():
            print(f"{row['ticker']:8} | Price: ${row['close']:8.2f} | Daily: {row['change_percent']:+7.2f}% | YoY: {row['yoy_return_percent']:+7.2f}% | PE: {row['pe_ratio']:6.2f} | Div: {row['dividend_yield']:5.2f}% | Score: {row['score']:5.1f}")

        # Bottom performers
        print("\n" + "-"*80)
        print("BOTTOM 10 PERFORMERS (by YoY Return)")
        print("-"*80)

        bottom_performers = df.nsmallest(10, "yoy_return_percent")[
            ["ticker", "close", "change_percent", "yoy_return_percent", "pe_ratio", "dividend_yield", "score"]
        ]

        for idx, row in bottom_performers.iterrows():
            print(f"{row['ticker']:8} | Price: ${row['close']:8.2f} | Daily: {row['change_percent']:+7.2f}% | YoY: {row['yoy_return_percent']:+7.2f}% | PE: {row['pe_ratio']:6.2f} | Div: {row['dividend_yield']:5.2f}% | Score: {row['score']:5.1f}")

        # Value stocks (low PE, good dividend)
        print("\n" + "-"*80)
        print("VALUE STOCKS (PE < 20 & Dividend > 2%)")
        print("-"*80)

        value_stocks = df[(df["pe_ratio"] < 20) & (df["dividend_yield"] > 2)].sort_values("score", ascending=False)

        if not value_stocks.empty:
            for idx, row in value_stocks.iterrows():
                print(f"{row['ticker']:8} | Price: ${row['close']:8.2f} | PE: {row['pe_ratio']:6.2f} | Div: {row['dividend_yield']:5.2f}% | Score: {row['score']:5.1f}")
        else:
            print("No value stocks found matching criteria.")

        # Growth stocks (high earnings growth)
        print("\n" + "-"*80)
        print("GROWTH STOCKS (YoY Return > 20%)")
        print("-"*80)

        growth_stocks = df[df["yoy_return_percent"] > 20].sort_values("yoy_return_percent", ascending=False)

        if not growth_stocks.empty:
            for idx, row in growth_stocks.iterrows():
                print(f"{row['ticker']:8} | Price: ${row['close']:8.2f} | YoY: {row['yoy_return_percent']:+7.2f}% | Score: {row['score']:5.1f}")
        else:
            print("No growth stocks found matching criteria.")

        # Export to CSV
        output_file = f"stock_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_export = df[[
            "ticker", "date", "open", "close", "change_percent",
            "yoy_return_percent", "52w_high", "52w_low",
            "pe_ratio", "dividend_yield", "eps", "score"
        ]]
        df_export.to_csv(output_file, index=False)

        print("\n" + "-"*80)
        print(f"[DONE] Report saved to: {output_file}")
        print("="*80 + "\n")

        return df

    def quick_scan(self, limit=10):
        """Quick scan of top opportunities"""
        print("\nQUICK MARKET SCAN")
        print("-" * 80)

        all_data = []

        for ticker in ALL_TICKERS[:limit]:
            daily = self.get_daily_prices(ticker)
            yoy = self.get_yoy_metrics(ticker)
            fundamentals = self.get_fundamentals(ticker)

            if daily and yoy and fundamentals:
                ticker_data = {**daily, **yoy, **fundamentals}
                ticker_data["score"] = self.score_stock(fundamentals)
                all_data.append(ticker_data)

        if not all_data:
            print("No data available.")
            return

        df = pd.DataFrame(all_data)
        df = df.sort_values("score", ascending=False)

        print(f"\nTop {len(df)} by Score:")
        for idx, row in df.head(10).iterrows():
            print(f"{row['ticker']:8} | ${row['close']:8.2f} | Score: {row['score']:5.1f} | YoY: {row['yoy_return_percent']:+7.2f}%")

        print("-" * 80 + "\n")


if __name__ == "__main__":
    screener = StockScreener()
    screener.generate_daily_report()
