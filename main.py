"""
Main Orchestration Script - Stocks Management Pipeline
"""

from data_collection import DataCollector
from analysis import StockAnalyzer
from database_manager import DatabaseManager
from datetime import datetime
import argparse


def full_pipeline():
    """Run complete pipeline: fetch data -> analyze -> generate signals"""
    print("=" * 60)
    print("STOCKS MANAGEMENT PIPELINE - FULL RUN")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: Collect data
    print("\n[1/3] Collecting stock data from yfinance...")
    collector = DataCollector()
    collector.collect_all_data()

    # Step 2: Analyze stocks
    print("\n[2/3] Analyzing stocks and generating signals...")
    analyzer = StockAnalyzer()
    analyzer.analyze_all_stocks()

    # Step 3: Display results
    print("\n[3/3] Displaying results...")
    display_signals()

    print("\n" + "=" * 60)
    print(f"Pipeline completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def daily_update():
    """Quick daily update of prices and signals"""
    print("=" * 60)
    print("STOCKS MANAGEMENT PIPELINE - DAILY UPDATE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: Update prices
    print("\n[1/2] Updating daily price data...")
    collector = DataCollector()
    collector.update_daily_data()

    # Step 2: Regenerate signals
    print("\n[2/2] Regenerating signals...")
    analyzer = StockAnalyzer()
    analyzer.analyze_all_stocks()

    # Display
    display_signals()

    print("\n" + "=" * 60)
    print(f"Update completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def display_signals():
    """Display latest signals"""
    db = DatabaseManager()
    signals = db.get_latest_signals(days=7)

    print("\n📊 RECENT BUY/SELL SIGNALS (Last 7 days):")
    print("-" * 60)

    if not signals:
        print("No signals generated yet.")
        return

    buy_signals = [s for s in signals if s[1] == "BUY"]
    sell_signals = [s for s in signals if s[1] == "SELL"]

    if buy_signals:
        print(f"\n🟢 BUY SIGNALS ({len(buy_signals)}):")
        for signal in buy_signals[:10]:
            print(f"  {signal[0]:8} | {signal[2]:35} | Strength: {signal[3]:.1f}")

    if sell_signals:
        print(f"\n🔴 SELL SIGNALS ({len(sell_signals)}):")
        for signal in sell_signals[:10]:
            print(f"  {signal[0]:8} | {signal[2]:35} | Strength: {signal[3]:.1f}")

    print("\n" + "-" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stocks Management Pipeline")
    parser.add_argument(
        "--mode",
        choices=["full", "daily"],
        default="daily",
        help="Pipeline mode: 'full' for initial setup, 'daily' for updates"
    )

    args = parser.parse_args()

    if args.mode == "full":
        full_pipeline()
    else:
        daily_update()
