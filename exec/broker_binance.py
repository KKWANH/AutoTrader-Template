import ccxt, os, math

from dotenv import load_dotenv
load_dotenv()

def make_binance():
    return ccxt.binance({
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_API_SECRET"),
        "enableRateLimit": True,
        "options": {"defaultType":"spot"}
    })

def fetch_min_notional(exchange, symbol):
    m = exchange.market(symbol); info = m.get("info",{})
    for f in info.get("filters", []):
        if f.get("filterType") in ("MIN_NOTIONAL","NOTIONAL"):
            return float(f.get("minNotional", f.get("notional", 10)))
    return 10.0

def round_step(x, step):
    return math.floor(x/step)*step

def place_market_order(exchange, symbol, side, quote_amount):
    price = exchange.fetch_ticker(symbol)["last"]
    min_notional = fetch_min_notional(exchange, symbol)
    if quote_amount < min_notional:
        raise ValueError(f"quote_amount {quote_amount} < min_notional {min_notional}")
    market = exchange.market(symbol)
    step = float([f for f in market['info']['filters'] if f['filterType']=='LOT_SIZE'][0]['stepSize'])
    amount = round_step(quote_amount/price, step)
    return exchange.create_order(symbol, "market", side, amount)
