"""
Quick Entry Point - Run Stock Screener
Simply run: python run_screener.py
"""

import argparse
from screener import StockScreener
from analysis import StockAnalyzer
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Stock Screener - Simple daily reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_screener.py              # Full daily report
  python run_screener.py --quick      # Quick scan (5 stocks)
  python run_screener.py --analyze    # Generate buy/sell signals
        """
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick scan of top 10 stocks only"
    )

    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Generate buy/sell signals after screening"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Full screening + signals + dashboard ready"
    )

    args = parser.parse_args()

    screener = StockScreener()

    # Default: full report
    if args.quick:
        print("\n[QUICK SCAN]...\n")
        screener.quick_scan(limit=10)
    elif args.analyze:
        print("\n[RUNNING SCREENER + SIGNAL ANALYSIS]...\n")
        screener.generate_daily_report()
        print("\n[ANALYZING] Buy/sell signals...\n")
        analyzer = StockAnalyzer()
        analyzer.analyze_all_stocks()
    elif args.full:
        print("\n[FULL PIPELINE]...\n")
        screener.generate_daily_report()
        print("\n[ANALYZING] All stocks...\n")
        analyzer = StockAnalyzer()
        analyzer.analyze_all_stocks()
        print("\n[DONE] Pipeline complete! Run 'streamlit run dashboard.py' to view dashboard.")
    else:
        # Default: full report
        screener.generate_daily_report()


if __name__ == "__main__":
    main()
