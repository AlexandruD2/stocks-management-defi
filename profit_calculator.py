"""
Profit/Loss Per Day Calculator
Calculates daily P&L metrics from portfolio holdings
"""

import pandas as pd
from database_manager import DatabaseManager
from datetime import datetime, timedelta


class ProfitCalculator:
    def __init__(self):
        self.db = DatabaseManager()

    def calculate_daily_pnl(self, ticker, days=30):
        """
        Calculate daily profit/loss for a stock over N days
        Assumes buying at historical prices and tracking unrealized P&L
        """
        prices = self.db.get_daily_prices(ticker, days=days + 10)

        if not prices or len(prices) < 2:
            return None

        prices_df = pd.DataFrame(
            prices,
            columns=["Date", "Open", "Close", "High", "Low", "Volume"]
        )
        prices_df = prices_df.sort_values("Date")

        # Calculate daily metrics
        prices_df["Daily_PnL"] = prices_df["Close"].diff()
        prices_df["Daily_PnL_Pct"] = (prices_df["Close"].pct_change() * 100).round(2)
        prices_df["Cumulative_PnL"] = prices_df["Daily_PnL"].cumsum()
        prices_df["Cumulative_PnL_Pct"] = prices_df["Daily_PnL_Pct"].cumsum()

        return prices_df.tail(days)

    def get_portfolio_summary(self, days=30):
        """
        Calculate summary statistics for portfolio over N days
        """
        portfolio = self.db.get_portfolio()

        if not portfolio:
            return None

        summary_data = []

        for ticker, shares_owned, average_cost, date_added in portfolio:
            pnl_df = self.calculate_daily_pnl(ticker, days=days)

            if pnl_df is not None:
                current_price = pnl_df["Close"].iloc[-1]
                initial_price = pnl_df["Close"].iloc[0]

                position_value = shares_owned * current_price
                position_cost = shares_owned * average_cost
                unrealized_pnl = position_value - position_cost
                unrealized_pnl_pct = (unrealized_pnl / position_cost * 100) if position_cost > 0 else 0

                avg_daily_pnl = pnl_df["Daily_PnL"].mean()
                best_day = pnl_df["Daily_PnL"].max()
                worst_day = pnl_df["Daily_PnL"].min()
                profitable_days = len(pnl_df[pnl_df["Daily_PnL"] > 0])
                total_days = len(pnl_df)

                summary_data.append({
                    "Ticker": ticker,
                    "Shares": shares_owned,
                    "Cost Basis": average_cost,
                    "Current Price": current_price,
                    "Position Value": position_value,
                    "Unrealized P&L": unrealized_pnl,
                    "Unrealized %": unrealized_pnl_pct,
                    "Avg Daily P&L": avg_daily_pnl,
                    "Best Day": best_day,
                    "Worst Day": worst_day,
                    "Win Rate %": (profitable_days / total_days * 100) if total_days > 0 else 0,
                    "Days Analyzed": total_days,
                })

        if not summary_data:
            return None

        summary_df = pd.DataFrame(summary_data)
        return summary_df

    def get_stock_analysis(self, ticker, days=30):
        """
        Get detailed daily P&L analysis for a single stock
        """
        pnl_df = self.calculate_daily_pnl(ticker, days=days)

        if pnl_df is None:
            return None

        metrics = {
            "ticker": ticker,
            "days_analyzed": len(pnl_df),
            "start_price": pnl_df["Close"].iloc[0],
            "end_price": pnl_df["Close"].iloc[-1],
            "period_return_pct": ((pnl_df["Close"].iloc[-1] - pnl_df["Close"].iloc[0]) / pnl_df["Close"].iloc[0] * 100),
            "avg_daily_pnl": pnl_df["Daily_PnL"].mean(),
            "avg_daily_pnl_pct": pnl_df["Daily_PnL_Pct"].mean(),
            "best_day": pnl_df["Daily_PnL"].max(),
            "worst_day": pnl_df["Daily_PnL"].min(),
            "std_dev": pnl_df["Daily_PnL_Pct"].std(),
            "profitable_days": len(pnl_df[pnl_df["Daily_PnL"] > 0]),
            "losing_days": len(pnl_df[pnl_df["Daily_PnL"] < 0]),
            "win_rate": (len(pnl_df[pnl_df["Daily_PnL"] > 0]) / len(pnl_df) * 100) if len(pnl_df) > 0 else 0,
            "cumulative_pnl": pnl_df["Daily_PnL"].sum(),
            "cumulative_pnl_pct": pnl_df["Daily_PnL_Pct"].sum(),
        }

        return metrics, pnl_df

    def compare_portfolio_performance(self, days=30):
        """
        Compare performance across all portfolio holdings
        """
        portfolio = self.db.get_portfolio()

        if not portfolio:
            return None

        comparison_data = []

        for ticker, shares_owned, average_cost, date_added in portfolio:
            metrics, _ = self.get_stock_analysis(ticker, days=days)

            if metrics:
                comparison_data.append({
                    "Ticker": ticker,
                    "Period Return %": metrics["period_return_pct"],
                    "Avg Daily %": metrics["avg_daily_pnl_pct"],
                    "Win Rate": metrics["win_rate"],
                    "Std Dev": metrics["std_dev"],
                    "Best Day": metrics["best_day"],
                    "Cumulative Return": metrics["cumulative_pnl_pct"],
                })

        if not comparison_data:
            return None

        comparison_df = pd.DataFrame(comparison_data)
        return comparison_df.sort_values("Period Return %", ascending=False)


if __name__ == "__main__":
    calc = ProfitCalculator()

    # Example usage
    analysis, daily_df = calc.get_stock_analysis("AAPL", days=30)
    print("AAPL 30-Day Analysis:")
    print(f"  Period Return: {analysis['period_return_pct']:.2f}%")
    print(f"  Avg Daily: {analysis['avg_daily_pnl_pct']:.2f}%")
    print(f"  Win Rate: {analysis['win_rate']:.1f}%")
