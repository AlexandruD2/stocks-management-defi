"""
Configuration for Stocks Management System
"""

"""
Configuration for Stocks Management System
"""

# Comprehensive Industry-based ticker list (from Yahoo Finance categories)
TICKERS = {
    # Technology & Software
    "Software & IT Services": ["MSFT", "ORCL", "CRM", "ADBE", "INTU"],
    "Hardware & Semiconductors": ["AAPL", "NVDA", "AMD", "QCOM", "MU"],
    "Internet & Cloud": ["GOOGL", "META", "NFLX", "AMZN", "PYPL"],

    # Healthcare & Life Sciences
    "Pharmaceuticals": ["JNJ", "PFE", "MRK", "LLY", "ABBV"],
    "Healthcare Services": ["UNH", "CVS", "CIGNA", "HUM", "ANTM"],
    "Biotechnology": ["AMGN", "BIIB", "GILD", "VRTX", "MRNA"],
    "Medical Devices": ["MDT", "ISRG", "SYK", "ZBH", "ALGN"],

    # Financials
    "Banks - Large": ["JPM", "BAC", "WFC", "GS", "CITI"],
    "Banks - Regional": ["PNC", "TFC", "MTB", "FITB", "KEY"],
    "Insurance": ["BRK.B", "AXP", "MET", "PRU", "PGR"],
    "Asset Management": ["BLK", "SCHW", "CME", "ICE", "NDAQ"],

    # Industrials & Manufacturing
    "Aerospace & Defense": ["BA", "RTX", "LMT", "NOC", "GD"],
    "Industrial Equipment": ["CAT", "PALL", "ITW", "EMR", "SNV"],
    "Conglomerates": ["GE", "HON", "MMM", "BLK", "BLDR"],
    "Machinery": ["DE", "CNH", "AGCO", "RHI", "ATI"],

    # Energy & Utilities
    "Oil & Gas Integrated": ["XOM", "CVX", "MPC", "PSX", "VLO"],
    "Oil & Gas Exploration": ["EOG", "FF", "COP", "HES", "PXD"],
    "Electric Utilities": ["NEE", "DUK", "SO", "AEP", "EXC"],
    "Natural Gas Utilities": ["WEC", "EIX", "NWE", "ONE", "AWK"],
    "Renewable Energy": ["NEE", "RUN", "ENPH", "PLUG", "ICLN"],

    # Consumer Discretionary
    "Retail - General": ["AMZN", "TJX", "TSCO", "COST", "WMT"],
    "Specialty Retail": ["HD", "LOW", "NWL", "ROST", "FIVE"],
    "Apparel & Footwear": ["NKE", "VFC", "DECK", "CROX", "SKX"],
    "Restaurants": ["MCD", "YUM", "SBUX", "CMG", "TXRH"],
    "Hotels & Lodging": ["MAR", "HLT", "RCI", "IHG", "CHDN"],

    # Consumer Staples
    "Food & Beverages": ["PEP", "KO", "MO", "KHC", "MDLZ"],
    "Consumer Packaged Goods": ["PG", "UL", "CL", "KMB", "SCPL"],
    "Grocery Stores": ["KR", "SFM", "CALLYY", "WBA", "AMPH"],

    # Communication & Media
    "Telecommunications": ["VZ", "T", "TMUS", "CMCSA", "CHTR"],
    "Media & Broadcasting": ["DIS", "PARA", "FOXA", "FUBO", "IMAX"],
    "Publishing": ["NYT", "GCI", "SAGE", "RELX", "TYP"],

    # Real Estate & Construction
    "Real Estate (REITs)": ["AMT", "PLD", "CCI", "WELL", "EQIX"],
    "Homebuilding": ["PHM", "LEN", "KB", "TOL", "DHI"],
    "Construction & Engineering": ["VISI", "ORION", "MTZ", "SNA", "MAS"],

    # Materials & Chemicals
    "Metals & Mining": ["FCX", "NUE", "CLF", "RIO", "VALE"],
    "Chemicals": ["DOW", "LYB", "CC", "SMPL", "ECL"],
    "Steel": ["X", "STLD", "CMC", "ATI", "NUE"],

    # Transportation & Logistics
    "Airlines": ["DAL", "UAL", "AAL", "SAVE", "ALK"],
    "Railroads": ["UNP", "CSX", "NSC", "KSU", "CP"],
    "Shipping & Logistics": ["FDX", "UPS", "XPO", "LOGI", "JBLU"],

    # Diversified / Multi-Sector
    "Artificial Intelligence": ["NVDA", "TSLA", "PLTR", "AI", "UPST"],
    "Conglomerates & Diversified": ["BRK.B", "BLK", "SPY", "QQQ", "IVV"],
}

# Flatten ticker list
ALL_TICKERS = [ticker for industry_tickers in TICKERS.values() for ticker in industry_tickers]

# Remove duplicates while preserving order
ALL_TICKERS = list(dict.fromkeys(ALL_TICKERS))

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
