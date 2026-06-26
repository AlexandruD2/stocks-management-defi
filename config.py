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

# Company name mapping for better readability
TICKER_NAMES = {
    # Technology & Software
    "MSFT": "Microsoft", "ORCL": "Oracle", "CRM": "Salesforce", "ADBE": "Adobe", "INTU": "Intuit",
    "NOW": "ServiceNow", "WDAY": "Workday", "AVGO": "Broadcom", "SNPS": "Synopsys", "CDNS": "Cadence Design",
    "IBM": "IBM", "ACN": "Accenture", "CSCO": "Cisco Systems",

    # Hardware & Semiconductors
    "AAPL": "Apple", "NVDA": "NVIDIA", "AMD": "Advanced Micro Devices", "QCOM": "Qualcomm", "MU": "Micron Technology",
    "INTC": "Intel", "ASML": "ASML", "LRCX": "Lam Research", "MRVL": "Marvell Technology", "AMAT": "Applied Materials",
    "KLAC": "KLA", "MCHP": "Microchip Technology", "ON": "ON Semiconductor",

    # Internet & Cloud
    "GOOGL": "Alphabet (Google)", "META": "Meta Platforms", "NFLX": "Netflix", "AMZN": "Amazon", "PYPL": "PayPal",
    "BKNG": "Booking Holdings", "SHOP": "Shopify", "COIN": "Coinbase", "DDOG": "Datadog", "SNOW": "Snowflake",
    "CRWD": "CrowdStrike", "DOCN": "DigitalOcean",

    # Pharmaceuticals
    "JNJ": "Johnson & Johnson", "PFE": "Pfizer", "MRK": "Merck", "LLY": "Eli Lilly", "ABBV": "AbbVie",
    "AZN": "AstraZeneca", "BMY": "Bristol Myers Squibb", "AMGN": "Amgen", "TEVA": "Teva Pharmaceutical",
    "CELG": "Celgene", "GILD": "Gilead Sciences", "VRTX": "Vertex Pharmaceuticals",

    # Healthcare Services
    "UNH": "UnitedHealth Group", "CVS": "CVS Health", "CI": "Cigna", "HUM": "Humana", "ANTM": "Anthem",
    "WBA": "Walgreens Boots Alliance", "RCI": "Rogers Communications", "DIS": "Disney", "MPW": "Medical Properties",
    "LTC": "LTC Properties", "BDX": "Becton Dickinson",

    # Biotechnology
    "BIIB": "Biogen", "BGEN": "Biogen", "EXEL": "Exelixis", "REGN": "Regeneron", "ALNY": "Alnylam Pharmaceuticals",
    "CRSP": "CRISPR Therapeutics", "EDIT": "Editas Medicine", "BEAM": "Beam Therapeutics", "MRNA": "Moderna",

    # Medical Devices
    "MDT": "Medtronic", "ISRG": "Intuitive Surgical", "SYK": "Stryker", "ZBH": "Zimmer Biomet", "ALGN": "Align Technology",
    "DXCM": "DexCom", "LUMN": "Lumen Technologies", "PODD": "Insulet", "SENS": "Senseonics", "VEEV": "Veeva Systems", "POOL": "Pool Corporation",

    # Banks - Large
    "JPM": "JPMorgan Chase", "BAC": "Bank of America", "WFC": "Wells Fargo", "GS": "Goldman Sachs", "C": "Citigroup",
    "BLK": "BlackRock", "PNC": "PNC Financial", "TD": "Toronto-Dominion Bank", "RBC": "Royal Bank of Canada",
    "USB": "U.S. Bancorp", "SCHW": "Charles Schwab", "TROW": "T. Rowe Price",

    # Banks - Regional
    "ZION": "Zions Bancorporation", "CFG": "Citizens Financial", "NTRS": "Northern Trust", "HBAN": "Huntington Bancshares",
    "OZK": "Ozark Bancshares", "WAFD": "Washington Federal", "FITB": "Fifth Third Bancorp", "KEY": "KeyCorp", "MTB": "M&T Bank", "TFC": "Truist Financial",

    # Insurance
    "BRK.B": "Berkshire Hathaway B", "AXP": "American Express", "MET": "MetLife", "PRU": "Prudential Financial", "PGR": "Progressive",
    "ALL": "Allstate", "HIG": "Hartford Financial", "TRV": "Travelers", "AFL": "Aflac", "LPL": "LPL Financial", "LNC": "Lincoln National", "KKR": "KKR",

    # Asset Management
    "CME": "CME Group", "ICE": "Intercontinental Exchange", "NDAQ": "NASDAQ", "GLEIF": "Global Legal Entity Identifier Foundation",
    "AB": "AllianceBernstein", "VOYA": "Voya Financial", "AMG": "Affiliated Managers Group", "EQIX": "Equinix", "MAN": "ManpowerGroup",

    # Aerospace & Defense
    "BA": "Boeing", "RTX": "Raytheon Technologies", "LMT": "Lockheed Martin", "NOC": "Northrop Grumman", "GD": "General Dynamics",
    "AXON": "Axon Enterprise", "TDG": "TransDigm", "LDOS": "Leidos", "HWM": "Howmet Aerospace", "KTOS": "Kratos Defense", "VSAT": "Viasat",

    # Industrial Equipment
    "CAT": "Caterpillar", "PALL": "Pall Corporation", "ITW": "Illinois Tool Works", "EMR": "Emerson Electric", "SNV": "Sensormatic Electronics",
    "PH": "Parker Hannifin", "SPX": "SPX Corporation", "EPAC": "Emagin", "AGCO": "AGCO", "NVR": "NVR Inc", "TYL": "Tyler Technologies",

    # Conglomerates
    "GE": "General Electric", "HON": "Honeywell", "MMM": "3M", "BLDR": "Bluerock Residential", "TRMB": "Trimble", "RSG": "Republic Services",
    "WR": "Weir Group", "ALB": "Albemarle", "FLS": "Flowserve", "IEX": "IDEX", "XYL": "Xylem",

    # Machinery
    "DE": "Deere & Company", "CNH": "CNH Industrial", "RHI": "Rheinmetall", "ATI": "ATI Inc", "ATGE": "Altec Industries", "GNTX": "Gentex",
    "IDCC": "InterDigital", "JBGS": "Jbg Smith Properties", "LVS": "Las Vegas Sands",

    # Oil & Gas Integrated
    "XOM": "Exxon Mobil", "CVX": "Chevron", "MPC": "Marathon Petroleum", "PSX": "Phillips 66", "VLO": "Valero Energy",
    "EOG": "EOG Resources", "COP": "ConocoPhillips", "SLB": "Schlumberger", "HAL": "Halliburton", "OKE": "ONEOK", "MRO": "Marathon Oil", "FANG": "Diamondback Energy",

    # Oil & Gas Exploration
    "HES": "Hess", "PXD": "Pioneer Natural Resources", "EQT": "EQT Corporation", "NBLX": "Noble", "CEIX": "CONSOL Energy", "CPE": "Callon Petroleum", "AR": "Antero Resources",

    # Electric Utilities
    "NEE": "NextEra Energy", "DUK": "Duke Energy", "SO": "Southern Company", "AEP": "American Electric Power", "EXC": "Exelon",
    "XEL": "Xcel Energy", "ES": "Eversource Energy", "WEC": "WEC Energy", "DTE": "DTE Energy", "EIX": "Edison International", "PNW": "Pinnacle West", "CMS": "CMS Energy",

    # Natural Gas Utilities
    "ONE": "ONE Gas", "AWK": "American Water Works", "UGI": "UGI Corporation", "NI": "NiSource", "ETR": "Equitable Gas", "SR": "Spire Inc", "EQT": "EQT Corporation", "CTG": "Catcher Energy",

    # Renewable Energy
    "RUN": "Sunrun", "ENPH": "Enphase Energy", "PLUG": "Plug Power", "ICLN": "iClimate Clean Energy ETF", "SEDG": "SolarEdge", "CLNE": "Clean Energy Fuels",
    "FUV": "Arcimoto", "GPRE": "Green Plains Renewable Energy", "FUEL": "Fuel Tech", "CSIQ": "Canadian Solar",

    # Retail - General
    "TJX": "TJX Companies", "COST": "Costco", "WMT": "Walmart", "HD": "Home Depot", "LOW": "Lowe's", "BBY": "Best Buy",
    "DG": "Dollar General", "DLTR": "Dollar Tree", "ACI": "Arch Capital", "ULTA": "Ulta Beauty",

    # Specialty Retail
    "NWL": "Newell Brands", "ROST": "Ross Stores", "FIVE": "Five Below", "CASY": "Casey's General Stores", "PVH": "PVH Corp",

    # Apparel & Footwear
    "NKE": "Nike", "VFC": "V.F. Corporation", "DECK": "Deckers Outdoor", "CROX": "Crocs", "SKX": "Skechers",
    "LULU": "Lululemon", "CALV": "Calvin Klein", "GIII": "G-III Apparel", "CPRI": "Capri Holdings", "TPH": "Tapestry Inc",

    # Restaurants
    "MCD": "McDonald's", "YUM": "Yum! Brands", "SBUX": "Starbucks", "CMG": "Chipotle", "TXRH": "Texas Roadhouse",
    "BLMN": "Bloomin' Brands", "DIN": "DineEquity", "BJRI": "Brinker International", "RUTH": "Ruth's Hospitality", "WING": "Wingstop", "DINE": "Dine Global",

    # Hotels & Lodging
    "MAR": "Marriott International", "HLT": "Hilton", "RCI": "RCI Hospitality", "IHG": "InterContinental Hotels", "CHDN": "Choice Hotels",
    "HST": "Host Hotels", "PK": "Park Hotels", "STAY": "Xenia Hotels", "XHR": "Xenia Hotels", "AHT": "Ashford Hospitality", "XRT": "Xero Shoes",

    # Food & Beverages
    "PEP": "PepsiCo", "KO": "Coca-Cola", "MO": "Altria", "KHC": "Kraft Heinz", "MDLZ": "Mondelez", "PM": "Philip Morris",
    "STZ": "Constellation Brands", "MNST": "Monster Beverage", "BUD": "Anheuser-Busch", "TSN": "Tyson Foods", "JBLU": "JetBlue", "SJM": "Smucker",

    # Consumer Packaged Goods
    "PG": "Procter & Gamble", "UL": "Unilever", "CL": "Colgate-Palmolive", "KMB": "Kimberly-Clark", "EL": "Estée Lauder",
    "GIS": "General Mills", "CPB": "Campbell Soup", "HSY": "Hershey", "ETN": "Eaton", "DOOR": "Doo", "LB": "L Brands",

    # Grocery Stores
    "KR": "Kroger", "AMPH": "Amphenol", "ASGN": "Apex Group", "SFM": "SpartanNash", "IMKTA": "Imkta",
    "SPB": "Spectrum Brands", "APOG": "Apogee Enterprises", "SMPL": "Simple Green", "MNSO": "Miniso",

    # Telecommunications
    "VZ": "Verizon", "T": "AT&T", "TMUS": "T-Mobile", "CMCSA": "Comcast", "CHTR": "Charter Communications",
    "LUMN": "Lumen Technologies", "SHENF": "Shenandoah Telecommunications", "CABO": "Cabometrix", "CCOI": "Cogent Communications", "FTR": "Frontier Communications",

    # Media & Broadcasting
    "DIS": "Disney", "FOXA": "Fox Corporation", "FUBO": "Fubo", "IMAX": "IMAX", "VITAQ": "Vita Coco",
    "AMC": "AMC Entertainment", "PARA": "Paramount Global", "SONY": "Sony", "FNCL": "Financial Select Sector SPDR", "SIRI": "Sirius XM",

    # Publishing
    "NYT": "New York Times", "GCI": "Gannett", "RELX": "RELX", "RHI": "Rhino Media", "VYST": "Vast",
    "WWW": "World Wrestling Entertainment", "IIIN": "Investview Inc", "OMAB": "Omab Media",

    # Real Estate (REITs)
    "AMT": "American Tower", "PLD": "Prologis", "CCI": "Crown Castle", "WELL": "Welltower", "EQIX": "Equinix",
    "O": "Realty Income", "WY": "Weyerhaeuser", "DLR": "Digital Realty", "RXO": "RXO Inc", "PSA": "Public Storage", "AVB": "AvalonBay Communities", "KIM": "Kimco Realty",

    # Homebuilding
    "PHM": "PulteGroup", "LEN": "Lennar", "KB": "KB Home", "TOL": "Toll Brothers", "DHI": "D.R. Horton",
    "BLDR": "Bluerock Residential", "MTH": "M/I Homes", "KBH": "KB Home", "NVR": "NVR Inc", "MHO": "M/I Homes", "TPH": "Tapestry Inc",

    # Construction & Engineering
    "SNA": "Snap-on", "MAS": "Masco", "ROK": "Rockwell Automation", "XYL": "Xylem", "RSC": "Resources Connection",
    "FLS": "Flowserve", "TYL": "Tyler Technologies", "RBC": "Royal Bank of Canada", "BXC": "Borrego Solar", "ARCM": "Arch-Con Corp",

    # Metals & Mining
    "FCX": "Freeport-McMoRan", "NUE": "Nucor", "CLF": "Cleveland-Cliffs", "RIO": "Rio Tinto", "VALE": "Vale",
    "SCCO": "Southern Copper", "X": "United States Steel", "US": "U.S. Steel", "GLATF": "Glatfelter", "STLD": "Steel Dynamics", "RS": "Reliance Steel",

    # Chemicals
    "DOW": "Dow Inc", "LYB": "LyondellBasell", "ECL": "Ecolab", "APD": "Air Products & Chemicals", "MOS": "Mosaic Company",
    "CF": "CF Industries", "CTVA": "Corteva", "AXTA": "Axalta Coating", "ALB": "Albemarle", "WLK": "Westlake Chemical",

    # Steel
    "STLD": "Steel Dynamics", "X": "U.S. Steel", "MT": "Arcelor Mittal", "CLF": "Cleveland-Cliffs", "RELX": "RELX", "RS": "Reliance Steel", "TX": "Ternium", "ATI": "ATI Inc",

    # Airlines
    "DAL": "Delta Air Lines", "UAL": "United Airlines", "AAL": "American Airlines", "ALK": "Alaska Air", "ALGT": "Allegiant Air",
    "JBLU": "JetBlue", "LUV": "Southwest Airlines", "SKEW": "Skywest", "ULCC": "Frontier Airlines",

    # Railroads
    "UNP": "Union Pacific", "CSX": "CSX", "NSC": "Norfolk Southern", "KSU": "Kansas City Southern", "CP": "Canadian Pacific",
    "CNI": "Canadian National", "LRCX": "Lam Research", "CRAT": "Cratos",

    # Shipping & Logistics
    "FDX": "FedEx", "UPS": "United Parcel Service", "XPO": "XPO Logistics", "LOGI": "Logitech", "RPAY": "REPAY Holdings",
    "ODFL": "Old Dominion Freight", "CVLG": "Covenant Transportation",

    # Artificial Intelligence
    "TSLA": "Tesla", "PLTR": "Palantir", "AI": "C3 Metrics", "UPST": "Upstart", "SMCI": "Super Micro Computer", "GRAB": "Grab Holdings", "SQ": "Square",

    # Conglomerates & Diversified
    "SPY": "SPY ETF", "QQQ": "QQQ ETF", "IVV": "IVV ETF", "APO": "Apollo Global Management",
}

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
