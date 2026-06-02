"""
Configuration for Stocks Management System
"""

# Sector-based ticker list
TICKERS = {
    "Artificial Intelligence": ["NVDA", "TSLA", "PLTR", "AI", "UPST"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "LLY"],
    "Information Technology": ["AAPL", "MSFT", "GOOGL", "META", "IBM"],
    "Communication Services": ["DIS", "VZ", "T", "CMCSA", "FOX"],
    "Industrials": ["BA", "CAT", "GE", "HON", "RTX"],
    "Energy": ["XOM", "CVX", "COP", "MPC", "EOG"],
    "Utilities": ["NEE", "DUK", "SO", "AEP", "EXC"],
}

# Flatten ticker list
ALL_TICKERS = [ticker for sector_tickers in TICKERS.values() for ticker in sector_tickers]

# Signal thresholds
SIGNAL_THRESHOLDS = {
    "dividend_yield_change": 0.5,  # % change to trigger alert
    "price_sma_20": 20,            # Simple Moving Average (days)
    "price_sma_50": 50,            # Simple Moving Average (days)
    "pe_ratio_threshold": 25,      # High PE alert
    "earnings_surprise_threshold": 5,  # % surprise
}

# Database settings
DB_PATH = "database/stocks.db"

# Dashboard settings
DAYS_LOOKBACK = 252  # One year of trading days
DASHBOARD_REFRESH_INTERVAL = 3600  # 1 hour in seconds
