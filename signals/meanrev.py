import pandas as pd, pandas_ta as ta

def meanrev_signal(df: pd.DataFrame):
    rsi = ta.rsi(df.close, length=14).iloc[-1]
    if rsi < 15: return {"side":"buy","strength":0.4}
    if rsi > 85: return {"side":"sell","strength":0.4}
    return None
