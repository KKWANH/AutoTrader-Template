import pandas as pd, pandas_ta as ta

def trend_signal(df: pd.DataFrame):
    dc = ta.donchian(df.high, df.low, lower_length=20, upper_length=20)
    adx = ta.adx(df.high, df.low, df.close, length=14)['ADX_14']
    last = df.iloc[-1]; up = dc['DCH_20_20'][-1]; dn = dc['DCL_20_20'][-1]
    if last.close > up and adx.iloc[-1] > 25: return {"side":"buy","strength":0.6}
    if last.close < dn: return {"side":"sell","strength":0.6}
    return None
