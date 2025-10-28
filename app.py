import os, time, pandas as pd
from dotenv import load_dotenv
from universe.filter import load_whitelist
from exec.paper import PaperBroker
from exec.broker_binance import make_binance, place_market_order
from signals.trend import trend_signal
from signals.meanrev import meanrev_signal
from llm.checklist import llm_review

load_dotenv()
USE_PAPER = os.getenv("USE_PAPER","true").lower()=="true"

def fetch_ohlcv_binance(ex, symbol, timeframe="5m", limit=300):
    o = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(o, columns=["ts","open","high","low","close","volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms"); df.set_index("ts", inplace=True)
    return df

def main():
    wl = load_whitelist()
    ex = make_binance()
    broker = PaperBroker() if USE_PAPER else ex

    while True:
        for sym in wl:
            df = fetch_ohlcv_binance(ex, sym, "5m")
            sig = next((s for s in (trend_signal(df), meanrev_signal(df)) if s), None)
            if not sig: continue

            ctx = {"symbol":sym, "price":float(df.close.iloc[-1]), "signal":sig}
            review = llm_review(ctx)
            if review.violation: continue

            if USE_PAPER:
                broker.submit(sym, sig["side"], qty=0.0005, price=ctx["price"])
            else:
                if sig["side"]=="buy":
                    place_market_order(ex, sym, "buy", 11.0)  # 최소 노셔널 예시
                # Spot short selling is omitted (logic for selling existing holdings is needed)
            print(sym, sig, review.summary)
            time.sleep(1)
        time.sleep(5)

if __name__=="__main__":
    main()
