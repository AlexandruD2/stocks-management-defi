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
    "Pharmaceuticals": ["JNJ", "PFE", "MERCK", "LLY", "ABBV"],
    "Healthcare Services": ["UNH", "CVS", "CIGNA", "HUM", "AET"],
    "Biotechnology": ["AMGN", "BIIB", "GILD", "VRTX", "MRNA"],
    "Medical Devices": ["MEDTRONIC", "ISRG", "STRYKER", "ZBH", "ALGN"],

    # Financials
    "Banks - Large": ["JPM", "BAC", "WFC", "GS", "C"],
    "Banks - Regional": ["PNC", "TRUIST", "M&T", "FITB", "KEY"],
    "Insurance": ["BRK.B", "AXP", "MET", "PRU", "PGR"],
    "Asset Management": ["BLK", "SCHW", "CME", "ICE", "NDAQ"],

    # Industrials & Manufacturing
    "Aerospace & Defense": ["BA", "RTX", "LMT", "NOC", "GD"],
    "Industrial Equipment": ["CAT", "PALL", "ITW", "EMR", "SNPS"],
    "Conglomerates": ["GE", "HON", "3M", "MMM", "BLDR"],
    "Machinery": ["DEERE", "NFLX", "RHI", "AGCO", "CNH"],

    # Energy & Utilities
    "Oil & Gas Integrated": ["XOM", "CVX", "MPC", "PSX", "VLO"],
    "Oil & Gas Exploration": ["EOG", "FANG", "COP", "HES", "PXD"],
    "Electric Utilities": ["NEE", "DUK", "SO", "AEP", "EXC"],
    "Natural Gas Utilities": ["WEC", "EIX", "NWE", "ONE", "AWK"],
    "Renewable Energy": ["NEXTERA", "RUN", "ENPH", "PLUG", "CCIV"],

    # Consumer Discretionary
    "Retail - General": ["AMZN", "TJX", "TSCO", "COST", "WMT"],
    "Specialty Retail": ["HD", "LOW", "NWL", "ROST", "FIVE"],
    "Apparel & Footwear": ["NKE", "VF", "DECK", "CROX", "SKX"],
    "Restaurants": ["MCD", "YUM", "SBUX", "CMG", "TXRH"],
    "Hotels & Lodging": ["MAR", "HLT", "RCI", "IHG", "CHDN"],

    # Consumer Staples
    "Food & Beverages": ["PEP", "KO", "MO", "KHC", "MDLZ"],
    "Consumer Packaged Goods": ["PG", "UNILEVER", "CL", "KMB", "WMK"],
    "Grocery Stores": ["KROGER", "SPROUTS", "CALLYY", "WBA", "CVS"],

    # Communication & Media
    "Telecommunications": ["VZ", "T", "TMUS", "CMCSA", "CHTR"],
    "Media & Broadcasting": ["DIS", "PARA", "FOX", "FUBO", "IMAX"],
    "Publishing": ["NYT", "GCI", "SAGE", "RELX", "TYP"],

    # Real Estate & Construction
    "Real Estate (REITs)": ["AMT", "PLD", "CCI", "WELL", "EQIX"],
    "Homebuilding": ["PHM", "LEN", "KB", "TOLL", "TOL"],
    "Construction & Engineering": ["VINCI", "ORION", "MTZ", "SNA", "MAS"],

    # Materials & Chemicals
    "Metals & Mining": ["FCX", "NUCOR", "CLF", "RIO", "VALE"],
    "Chemicals": ["DOW", "LYB", "CC", "SMPL", "ECL"],
    "Steel": ["NUE", "X", "STLD", "CMC", "ATI"],

    # Transportation & Logistics
    "Airlines": ["DAL", "UAL", "AAL", "SAVE", "ALK"],
    "Railroads": ["UNP", "CSX", "NSC", "KSU", "CP"],
    "Shipping & Logistics": ["FDX", "UPS", "XPO", "LOGI", "JBLU"],

    # Diversified / Multi-Sector
    "Artificial Intelligence": ["NVDA", "TSLA", "PLTR", "AI", "UPST"],
    "Conglomerates & Diversified": ["BRK.B", "BERKSHIRE", "SPY", "QQQ", "IVV"],
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
