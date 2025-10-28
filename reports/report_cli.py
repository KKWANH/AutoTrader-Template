# reports/report_cli.py
import argparse, os, sys, sqlite3, math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

def load_trades(db_path, start, end):
    con = sqlite3.connect(db_path)
    q = """
    SELECT ts, symbol, side, qty, entry_price, exit_price, fee, pnl
    FROM trades
    WHERE ts BETWEEN ? AND ?;
    """
    df = pd.read_sql(q, con, params=[start, end], parse_dates=['ts'])
    con.close()
    return df.sort_values('ts')

def kpi(df: pd.DataFrame):
    if df.empty:
        return dict(trades=0, wins=0, losses=0, winrate=0.0, gross=0.0, fees=0.0,
                    net=0.0, pf=0.0, avg_trade=0.0, max_dd=0.0)
    gross = df['pnl'].sum()
    fees  = df['fee'].sum() if 'fee' in df else 0.0
    net   = gross - fees
    wins  = (df['pnl'] > 0).sum()
    losses= (df['pnl'] <=0).sum()
    wr    = wins / max(1,(wins+losses))
    # profit factor
    gross_pos = df.loc[df['pnl']>0,'pnl'].sum()
    gross_neg = -df.loc[df['pnl']<=0,'pnl'].sum()
    pf = (gross_pos / gross_neg) if gross_neg>0 else np.inf
    avg_trade = net / max(1,(wins+losses))
    # equity & max drawdown
    eq = df['pnl'].cumsum()
    rolling_max = eq.cummax()
    dd = (eq - rolling_max)
    max_dd = dd.min() if not dd.empty else 0.0
    return dict(trades=len(df), wins=wins, losses=losses, winrate=wr,
                gross=gross, fees=fees, net=net, pf=pf, avg_trade=avg_trade, max_dd=max_dd)

def equity_curve_plot(df, out_png):
    if df.empty:
        return
    eq = df[['ts','pnl']].copy()
    eq['equity'] = eq['pnl'].cumsum()
    plt.figure()
    plt.plot(eq['ts'], eq['equity'])
    plt.title("Equity Curve")
    plt.xlabel("Time"); plt.ylabel("Cumulative PnL")
    plt.tight_layout(); plt.savefig(out_png); plt.close()

def monthly_heatmap(df, out_png):
    if df.empty: return
    d = df.copy()
    d['date'] = d['ts'].dt.date
    gp = d.groupby(['date'])['pnl'].sum()
    # calendar-like heatmap 대용: 막대
    plt.figure()
    gp.plot(kind='bar')
    plt.title("Daily PnL")
    plt.xlabel("Date"); plt.ylabel("PnL")
    plt.tight_layout(); plt.savefig(out_png); plt.close()

def winloss_by_symbol(df, out_png):
    if df.empty: return
    gp = df.groupby('symbol')['pnl'].sum().sort_values(ascending=False)
    plt.figure()
    gp.plot(kind='bar')
    plt.title("PnL by Symbol")
    plt.xlabel("Symbol"); plt.ylabel("PnL")
    plt.tight_layout(); plt.savefig(out_png); plt.close()

def to_markdown_table(k):
    return (
f"""| Metric | Value |
|---|---:|
| Trades | {k['trades']} |
| Wins | {k['wins']} |
| Losses | {k['losses']} |
| Winrate | {k['winrate']:.2%} |
| Gross PnL | {k['gross']:.2f} |
| Fees | {k['fees']:.2f} |
| Net PnL | **{k['net']:.2f}** |
| Profit Factor | {k['pf']:.2f} |
| Avg/Trade | {k['avg_trade']:.2f} |
| Max Drawdown | {k['max_dd']:.2f} |
""")

def resolve_period(period):
    now = datetime.utcnow()
    if period=="daily":
        start = (now - timedelta(days=1)).replace(hour=0,minute=0,second=0,microsecond=0)
        end   = start + timedelta(days=1)
    elif period=="weekly":
        # 지난 주 월~일
        wd = now.weekday()
        end = datetime(now.year, now.month, now.day) - timedelta(days=wd+1)
        start = end - timedelta(days=6)
        end = end + timedelta(days=1)
    elif period=="monthly":
        first = datetime(now.year, now.month, 1)
        start = first - timedelta(days=1)
        start = datetime(start.year, start.month, 1)
        end   = first
    else:
        raise SystemExit("period must be one of: daily/weekly/monthly or use --from --to")
    return start, end

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/trades.sqlite")
    ap.add_argument("--period", choices=["daily","weekly","monthly"])
    ap.add_argument("--from", dest="dfrom")
    ap.add_argument("--to", dest="dto")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    if args.period:
        start, end = resolve_period(args.period)
    else:
        if not (args.dfrom and args.dto):
            raise SystemExit("Use --period or both --from and --to (YYYY-MM-DD).")
        start = datetime.fromisoformat(args.dfrom)
        end   = datetime.fromisoformat(args.dto)

    outdir = args.outdir or f"reports/{datetime.utcnow().strftime('%Y-%m-%d')}"
    Path(outdir).mkdir(parents=True, exist_ok=True)
    df = load_trades(args.db, start, end)

    # KPIs
    k = kpi(df)
    md = to_markdown_table(k)
    # 저장
    df.to_csv(f"{outdir}/trades_raw.csv", index=False)
    with open(f"{outdir}/summary.md","w",encoding="utf-8") as f:
        f.write(f"# Summary ({start.date()} ~ {end.date()})\n\n")
        f.write(md)

    # 그래프
    Path(f"{outdir}/fig").mkdir(exist_ok=True)
    equity_curve_plot(df, f"{outdir}/fig/equity_curve.png")
    monthly_heatmap(df, f"{outdir}/fig/daily_pnl.png")
    winloss_by_symbol(df, f"{outdir}/fig/pnl_by_symbol.png")

    print(f"[report] generated at {outdir}")

if __name__=="__main__":
    main()
