# Major Indian Stocks (NSE)
INDIAN_STOCKS = {
    # Banking & Finance
    "SBIN": "State Bank of India",
    "HDFC": "HDFC Bank",
    "ICICIBANK": "ICICI Bank",
    "AXISBANK": "Axis Bank",
    "KOTAKBANK": "Kotak Mahindra Bank",
    "INDUSIND": "IndusInd Bank",
    "HDFCBANK": "HDFC Bank Limited",
    "FEDERALBNK": "Federal Bank",
    "IDFCFIRSTB": "IDFC First Bank",
    "AUBANK": "AU Small Finance Bank",
    "BANDHANBNK": "Bandhan Bank",
    "YESBANK": "Yes Bank",
    "SUNPHARMA": "Sun Pharma",
    
    # IT & Tech
    "TCS": "Tata Consultancy Services",
    "INFOSYS": "Infosys",
    "WIPRO": "Wipro",
    "HCLTECH": "HCL Technologies",
    "INFY": "Infosys",
    "TECH": "Tech Companies",
    
    # Energy & Power
    "RELIANCE": "Reliance Industries",
    "NTPC": "National Thermal Power Corporation",
    "POWERGRID": "Power Grid",
    "IOC": "Indian Oil Corporation",
    "BPCL": "Bharat Petroleum",
    "HINDALCO": "Hindalco Industries",
    "COALINDIA": "Coal India",
    "GAIL": "GAIL (India)",
    
    # Automotive
    "MARUTI": "Maruti Suzuki",
    "BAJAJAUT": "Bajaj Auto",
    "MAHINDRA": "Mahindra & Mahindra",
    "TATAMOTORS": "Tata Motors",
    "HEROMOTOCO": "Hero MotoCorp",
    "SUNRISETEL": "Sunrise Technologies",
    
    # Pharma
    "DRREDDY": "Dr. Reddy's Labs",
    "CIPLA": "Cipla",
    "LUPIN": "Lupin",
    "BIOCON": "Biocon",
    "CADILAHC": "Cadila Healthcare",
    "ALKEM": "Alkem Laboratories",
    "ASTRAZEN": "AstraZeneca Pharma",
    
    # FMCG
    "ITC": "ITC",
    "NESTLEIND": "Nestle India",
    "HINDUNILVR": "Hindustan Unilever",
    "BRITANNIA": "Britannia",
    "DABUR": "Dabur India",
    "MARICO": "Marico",
    "COLPAL": "Colgate-Palmolive",
    
    # Telecom
    "AIRTELGROUP": "Airtel Group",
    "JIO": "Jio (Reliance Jio)",
    "VODAFONE": "Vodafone Idea",
    "BSNL": "BSNL",
    
    # Real Estate & Construction
    "BHARTIARTL": "Bharti Airtel",
    "ADANIPORTS": "Adani Ports",
    "ADANIPOWER": "Adani Power",
    "ADANIGREEN": "Adani Green Energy",
    "DLF": "DLF",
    "LODHA": "Lodha Group",
    "OBEROIRLTY": "Oberoi Realty",
    
    # Consumer Durables
    "HAVELLS": "Havells",
    "SIEMENS": "Siemens",
    "WHIRLPOOL": "Whirlpool",
    "BOSCHLTD": "Bosch",
    
    # Cement
    "ULTRACEMCO": "UltraTech Cement",
    "SHREECEM": "Shree Cement",
    "AMBUJACEMENT": "Ambuja Cements",
    "ACC": "ACC",
    
    # Steel
    "TATASTEEL": "Tata Steel",
    "SAILIND": "SAIL",
    "JSWSTEEL": "JSW Steel",
    "NATIONALSTL": "National Steel",
    
    # Others
    "BAJAJFINSV": "Bajaj Finserv",
    "BAJAJFINANC": "Bajaj Finance",
    "ICICIPRULI": "ICICI Prudential",
    "HDFC": "HDFC",
    "M&M": "Mahindra & Mahindra",
    "LT": "Larsen & Toubro",
    "KPRMILL": "KPR Mill",
    "ONGC": "ONGC",
}

# Major Cryptocurrencies
CRYPTO_COINS = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "BNB-USD": "Binance Coin",
    "XRP-USD": "Ripple (XRP)",
    "ADA-USD": "Cardano",
    "SOL-USD": "Solana",
    "DOGE-USD": "Dogecoin",
    "DOT-USD": "Polkadot",
    "LINK-USD": "Chainlink",
    "MATIC-USD": "Polygon (Matic)",
    "AVAX-USD": "Avalanche",
    "LTC-USD": "Litecoin",
    "ATOM-USD": "Cosmos",
    "VET-USD": "VeChain",
    "UNI-USD": "Uniswap",
    "AAVE-USD": "Aave",
    "SUSHI-USD": "Sushi",
    "FTX-USD": "FTX Token",
    "ARB-USD": "Arbitrum",
    "OP-USD": "Optimism",
    "STETH-USD": "Staked Ethereum",
    "USDC-USD": "USD Coin",
    "USDT-USD": "Tether",
    "DAI-USD": "Dai",
    "XLM-USD": "Stellar Lumens",
    "ALGO-USD": "Algorand",
    "CRO-USD": "Crypto.com Coin",
    "ICP-USD": "Internet Computer",
    "APE-USD": "ApeCoin",
}

# Special Options
SPECIAL_SYMBOLS = {
    "NIFTY50": "Nifty 50 Index",
    "SENSEX": "BSE Sensex",
    "NIFTYIT": "Nifty IT Index",
    "NIFTYBANK": "Nifty Bank Index",
    "CASH": "Cash / Money Market",
    "GOLD": "Gold",
    "SILVER": "Silver",
}

# Combined list of all symbols with names
ALL_SYMBOLS = {
    **INDIAN_STOCKS,
    **CRYPTO_COINS,
    **SPECIAL_SYMBOLS,
}

def get_all_symbols():
    """Get all available symbols for display"""
    return sorted(ALL_SYMBOLS.keys())

def get_symbol_description(symbol):
    """Get description for a symbol"""
    return ALL_SYMBOLS.get(symbol, symbol)

def get_symbols_by_category():
    """Get symbols grouped by category"""
    return {
        "Indian Stocks": INDIAN_STOCKS,
        "Cryptocurrencies": CRYPTO_COINS,
        "Indices & Special": SPECIAL_SYMBOLS,
    }

def format_symbol_option(symbol):
    """Format symbol for display in dropdown"""
    description = get_symbol_description(symbol)
    return f"{symbol} - {description}"
