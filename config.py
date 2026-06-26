"""
Configuration for Stocks Management System
Expanded industry coverage with 12-15 stocks per category
"""

# Comprehensive Industry-based ticker list (from Yahoo Finance categories)
TICKERS = {
    # Technology & Software
    "Software & IT Services": ["MSFT", "ORCL", "CRM", "ADBE", "INTU", "NOW", "WDAY", "AVGO", "SNPS", "CDNS", "IBM", "ACN", "CSCO"],
    "Hardware & Semiconductors": ["AAPL", "NVDA", "AMD", "QCOM", "MU", "INTC", "ASML", "LRCX", "MRVL", "AMAT", "KLAC", "MCHP", "ON"],
    "Internet & Cloud": ["GOOGL", "META", "NFLX", "AMZN", "PYPL", "BKNG", "SHOP", "COIN", "DDOG", "SNOW", "CRWD", "CRM", "DOCN"],

    # Healthcare & Life Sciences
    "Pharmaceuticals": ["JNJ", "PFE", "MRK", "LLY", "ABBV", "AZN", "BMY", "AMGN", "TEVA", "CELG", "GILD", "VRTX"],
    "Healthcare Services": ["UNH", "CVS", "CI", "HUM", "ANTM", "WBA", "RCI", "DIS", "MPW", "LTC", "BDX"],
    "Biotechnology": ["AMGN", "BIIB", "GILD", "VRTX", "MRNA", "BGEN", "EXEL", "REGN", "ALNY", "CRSP", "EDIT", "BEAM"],
    "Medical Devices": ["MDT", "ISRG", "SYK", "ZBH", "ALGN", "DXCM", "LUMN", "PODD", "SENS", "VEEV", "POOL"],

    # Financials
    "Banks - Large": ["JPM", "BAC", "WFC", "GS", "C", "BLK", "PNC", "TD", "RBC", "USB", "SCHW", "TROW"],
    "Banks - Regional": ["PNC", "TFC", "MTB", "FITB", "KEY", "ZION", "CFG", "NTRS", "HBAN", "OZK", "WAFD", "CBRL"],
    "Insurance": ["BRK.B", "AXP", "MET", "PRU", "PGR", "ALL", "HIG", "TRV", "AFL", "LPL", "LNC", "KKR"],
    "Asset Management": ["BLK", "SCHW", "CME", "ICE", "NDAQ", "GLEIF", "AB", "VOYA", "AMG", "EQIX", "MAN"],

    # Industrials & Manufacturing
    "Aerospace & Defense": ["BA", "RTX", "LMT", "NOC", "GD", "AXON", "TDG", "LDOS", "HWM", "KTOS", "VSAT"],
    "Industrial Equipment": ["CAT", "PALL", "ITW", "EMR", "SNV", "PH", "SPX", "EPAC", "AGCO", "NVR", "TYL"],
    "Conglomerates": ["GE", "HON", "MMM", "BLDR", "TRMB", "RSG", "WR", "ALB", "FLS", "IEX", "XYL"],
    "Machinery": ["DE", "CNH", "AGCO", "RHI", "ATI", "ATGE", "GNTX", "IDCC", "JBGS", "LVS"],

    # Energy & Utilities
    "Oil & Gas Integrated": ["XOM", "CVX", "MPC", "PSX", "VLO", "EOG", "COP", "SLB", "HAL", "OKE", "MRO", "FANG"],
    "Oil & Gas Exploration": ["EOG", "COP", "HES", "PXD", "FANG", "EQT", "OKE", "NBLX", "CEIX", "CPE", "AR"],
    "Electric Utilities": ["NEE", "DUK", "SO", "AEP", "EXC", "XEL", "ES", "WEC", "DTE", "EIX", "PNW", "CMS"],
    "Natural Gas Utilities": ["WEC", "EIX", "NWE", "ONE", "AWK", "UGI", "NI", "ETR", "SR", "EQT", "CTG"],
    "Renewable Energy": ["NEE", "RUN", "ENPH", "PLUG", "ICLN", "SEDG", "CLNE", "FUV", "GPRE", "FUEL", "CSIQ"],

    # Consumer Discretionary
    "Retail - General": ["AMZN", "TJX", "COST", "WMT", "HD", "LOW", "BBY", "DG", "DLTR", "FIVE", "ACI", "ULTA"],
    "Specialty Retail": ["HD", "LOW", "NWL", "ROST", "FIVE", "BBY", "DG", "DLTR", "ACI", "ULTA", "CASY", "PVH"],
    "Apparel & Footwear": ["NKE", "VFC", "DECK", "CROX", "SKX", "LULU", "CALV", "KKR", "GIII", "CPRI", "TPH"],
    "Restaurants": ["MCD", "YUM", "SBUX", "CMG", "TXRH", "BLMN", "DIN", "BJRI", "RUTH", "WING", "DINE"],
    "Hotels & Lodging": ["MAR", "HLT", "RCI", "IHG", "CHDN", "HST", "PK", "STAY", "XHR", "AHT", "XRT"],

    # Consumer Staples
    "Food & Beverages": ["PEP", "KO", "MO", "KHC", "MDLZ", "PM", "STZ", "MNST", "BUD", "TSN", "JBLU", "SJM"],
    "Consumer Packaged Goods": ["PG", "UL", "CL", "KMB", "EL", "GIS", "CPB", "HSY", "ETN", "DOOR", "LB"],
    "Grocery Stores": ["KR", "WBA", "AMPH", "ASGN", "SFM", "IMKTA", "SPB", "APOG", "SMPL", "MNSO"],

    # Communication & Media
    "Telecommunications": ["VZ", "T", "TMUS", "CMCSA", "CHTR", "LUMN", "SHENF", "CABO", "CCOI", "FTR"],
    "Media & Broadcasting": ["DIS", "FOXA", "FUBO", "IMAX", "VITAQ", "AMC", "PARA", "SONY", "FNCL", "SIRI"],
    "Publishing": ["NYT", "GCI", "RELX", "RHI", "VYST", "WWW", "IIIN", "OMAB"],

    # Real Estate & Construction
    "Real Estate (REITs)": ["AMT", "PLD", "CCI", "WELL", "EQIX", "O", "WY", "DLR", "RXO", "PSA", "AVB", "KIM"],
    "Homebuilding": ["PHM", "LEN", "KB", "TOL", "DHI", "BLDR", "MTH", "KBH", "NVR", "MHO", "TPH"],
    "Construction & Engineering": ["SNA", "MAS", "ROK", "XYL", "RSC", "FLS", "TYL", "RBC", "BXC", "ARCM"],

    # Materials & Chemicals
    "Metals & Mining": ["FCX", "NUE", "CLF", "RIO", "VALE", "SCCO", "X", "US", "GLATF", "STLD", "RS"],
    "Chemicals": ["DOW", "LYB", "ECL", "APD", "MOS", "CF", "CTVA", "AXTA", "ALB", "WLK"],
    "Steel": ["STLD", "NUE", "X", "MT", "CLF", "RELX", "RS", "TX", "ATI"],

    # Transportation & Logistics
    "Airlines": ["DAL", "UAL", "AAL", "ALK", "ALGT", "JBLU", "LUV", "SKEW", "ULCC"],
    "Railroads": ["UNP", "CSX", "NSC", "KSU", "CP", "CNI", "LRCX", "CRAT"],
    "Shipping & Logistics": ["FDX", "UPS", "XPO", "LOGI", "JBLU", "RPAY", "ODFL", "CVLG"],

    # Diversified / Multi-Sector
    "Artificial Intelligence": ["NVDA", "TSLA", "PLTR", "AI", "UPST", "MRVL", "SMCI", "GRAB", "SQ", "COIN"],
    "Conglomerates & Diversified": ["BRK.B", "BLK", "SPY", "QQQ", "IVV", "GE", "HON", "MMM", "ITW", "APO"],
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
