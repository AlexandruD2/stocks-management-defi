"""
Stock Analysis and Signal Generation
"""

import pandas as pd
import numpy as np
from database_manager import DatabaseManager
from config import SIGNAL_THRESHOLDS, ALL_TICKERS
from datetime import datetime


class StockAnalyzer:
    def __init__(self):
        self.db = DatabaseManager()

    def calculate_moving_averages(self, ticker, periods=[20, 50, 200]):
        """Calculate moving averages for a stock"""
        prices = self.db.get_daily_prices(ticker, days=250)
        if not prices:
            return None

        df = pd.DataFrame(prices, columns=["date", "open", "close", "high", "low", "volume"])
        df = df.sort_values("date")

        result = {"ticker": ticker, "date": df.iloc[-1]["date"]}

        for period in periods:
            ma = df["close"].tail(period).mean()
            result[f"sma_{period}"] = ma

        # Get current price
        result["current_price"] = df.iloc[-1]["close"]

        return result

    def generate_moving_average_signal(self, ticker):
        """Generate BUY/SELL signal based on moving averages"""
        ma_data = self.calculate_moving_averages(ticker)
        if not ma_data:
            return None

        current = ma_data["current_price"]
        sma_20 = ma_data["sma_20"]
        sma_50 = ma_data["sma_50"]
        sma_200 = ma_data["sma_200"]

        # Golden Cross (20 > 50 > 200) = BUY
        # Death Cross (20 < 50 < 200) = SELL
        if sma_20 > sma_50 > sma_200:
            strength = min(100, (sma_20 - sma_200) / sma_200 * 100)
            return {
                "signal": "BUY",
                "reason": "moving_average_golden_cross",
                "strength": strength
            }
        elif sma_20 < sma_50 < sma_200:
            strength = min(100, (sma_200 - sma_20) / sma_200 * 100)
            return {
                "signal": "SELL",
                "reason": "moving_average_death_cross",
                "strength": strength
            }

        # Price above SMA20 = bullish
        if current > sma_20:
            strength = (current - sma_20) / sma_20 * 100
            return {
                "signal": "BUY",
                "reason": "price_above_sma20",
                "strength": min(50, strength)
            }
        else:
            strength = (sma_20 - current) / sma_20 * 100
            return {
                "signal": "SELL",
                "reason": "price_below_sma20",
                "strength": min(50, strength)
            }

    def analyze_dividend_yield(self, ticker):
        """Analyze dividend yield trend"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT date, dividend_yield FROM fundamentals
            WHERE ticker = ?
            ORDER BY date DESC
            LIMIT 90
        """, (ticker,))

        data = cursor.fetchall()
        conn.close()

        if len(data) < 2:
            return None

        latest_yield = data[0][1]
        previous_yield = data[-1][1]

        if latest_yield is None or previous_yield is None:
            return None

        yield_change = ((latest_yield - previous_yield) / previous_yield * 100) if previous_yield > 0 else 0

        # High dividend yield (>2.5%) with increasing trend = BUY
        if latest_yield > 2.5 and yield_change > SIGNAL_THRESHOLDS["dividend_yield_change"]:
            return {
                "signal": "BUY",
                "reason": "dividend_yield_increase",
                "strength": min(70, 50 + abs(yield_change))
            }
        # Decreasing dividend yield = SELL signal
        elif yield_change < -SIGNAL_THRESHOLDS["dividend_yield_change"]:
            return {
                "signal": "SELL",
                "reason": "dividend_yield_decrease",
                "strength": min(70, 50 + abs(yield_change))
            }

        return None

    def analyze_earnings_quality(self, ticker):
        """Analyze earnings surprises"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT eps_actual, eps_estimate, surprise_percent
            FROM earnings
            WHERE ticker = ?
            ORDER BY date DESC
            LIMIT 5
        """, (ticker,))

        earnings = cursor.fetchall()
        conn.close()

        if not earnings:
            return None

        # Check for consistent positive surprises
        positive_surprises = sum(1 for e in earnings if e[2] and e[2] > SIGNAL_THRESHOLDS["earnings_surprise_threshold"])

        if positive_surprises >= 3:
            avg_surprise = np.mean([e[2] for e in earnings if e[2]])
            return {
                "signal": "BUY",
                "reason": "consistent_positive_earnings",
                "strength": min(80, 50 + avg_surprise)
            }

        # Check for negative trend
        negative_surprises = sum(1 for e in earnings if e[2] and e[2] < -SIGNAL_THRESHOLDS["earnings_surprise_threshold"])

        if negative_surprises >= 2:
            return {
                "signal": "SELL",
                "reason": "negative_earnings_surprise",
                "strength": 60
            }

        return None

    def analyze_valuation(self, ticker):
        """Analyze stock valuation (PE ratio)"""
        fundamentals = self.db.get_latest_fundamentals(ticker)

        if not fundamentals or fundamentals[3] is None:  # pe_ratio is index 3
            return None

        pe = fundamentals[3]

        if pe < 15:
            return {
                "signal": "BUY",
                "reason": "low_pe_valuation",
                "strength": 70
            }
        elif pe > SIGNAL_THRESHOLDS["pe_ratio_threshold"]:
            return {
                "signal": "SELL",
                "reason": "high_pe_valuation",
                "strength": 50
            }

        return None

    def generate_comprehensive_signal(self, ticker):
        """Generate a comprehensive signal from all analyses"""
        signals = []

        # Collect all signals
        ma_signal = self.generate_moving_average_signal(ticker)
        if ma_signal:
            signals.append(("moving_average", ma_signal))

        div_signal = self.analyze_dividend_yield(ticker)
        if div_signal:
            signals.append(("dividend", div_signal))

        earn_signal = self.analyze_earnings_quality(ticker)
        if earn_signal:
            signals.append(("earnings", earn_signal))

        val_signal = self.analyze_valuation(ticker)
        if val_signal:
            signals.append(("valuation", val_signal))

        if not signals:
            return None

        # Aggregate signals
        buy_strength = sum(s[1]["strength"] for s in signals if s[1]["signal"] == "BUY") / len(signals)
        sell_strength = sum(s[1]["strength"] for s in signals if s[1]["signal"] == "SELL") / len(signals)

        if buy_strength > sell_strength:
            primary_reason = [s[1]["reason"] for s in signals if s[1]["signal"] == "BUY"][0]
            return {
                "signal": "BUY",
                "reason": primary_reason,
                "strength": min(100, buy_strength)
            }
        else:
            primary_reason = [s[1]["reason"] for s in signals if s[1]["signal"] == "SELL"][0]
            return {
                "signal": "SELL",
                "reason": primary_reason,
                "strength": min(100, sell_strength)
            }

    def analyze_all_stocks(self):
        """Generate signals for all stocks"""
        print("Analyzing all stocks...")

        for ticker in ALL_TICKERS:
            signal = self.generate_comprehensive_signal(ticker)
            if signal:
                self.db.insert_signal(
                    ticker,
                    signal["signal"],
                    signal["reason"],
                    signal["strength"]
                )
                print(f"  {ticker}: {signal['signal']} ({signal['reason']}) - Strength: {signal['strength']:.1f}")

        print("Analysis complete!")


if __name__ == "__main__":
    analyzer = StockAnalyzer()
    analyzer.analyze_all_stocks()
