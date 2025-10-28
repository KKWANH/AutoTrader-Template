# Welcome to AutoTrader-Template

> All investment decisions are the responsibility of the investor.
> This project provides an automated trading framework for research and educational purposes.

## Overview
AutoTradingProject is a lightweight, fully containerized automated trading system designed for
efficient deployment on low-cost VPS environments such as Contabo VPS S.
It integrates a local open-source LLM for daily/weekly/monthly risk analysis and report generation,
eliminating the need for expensive cloud APIs.

## Core Features
### Lightweight & Cost-Efficient
- Cheap hosting fee (Contabo VPS S)
- Open sourced LLM model
- Perform tasks based on programmed formulas
- Fast reaction speed

### High-Profit / Minimal-Risk Strategy
- Whitelist-based universe control rules
    - **Market capitalization**: Top 50, Liquidity and price manipulation prevention
    - **Trading volume**: Over $50 million in 24-hour trading volume, minimal slippage
    - **Exchange reliability**: Tier 1 exchanges such as Binance/OKX, minimal listing/trading risk
    - **Project age**: Over 1 year since launch, minimal Rug Pull risk
    - **Major wallet distribution**: Top 10 wallets < 40% of total, preventing minority dominance
    - **On-chain activity**: Recent transactions on Etherscan/Explorer, ghost project filtering
    - **DeFi and meme coins**: “High Risk” tag, only separate strategies allowed, small amounts for volatility ranges
    - **Stablecoins, LP tokens, wrapped tokens, test tokens, and automated trading**: excluded, not suitable for this purpose

### Local LLM integration
- Model: Phi-3 mini (default), Mistral 7B, or DeepSeek-R1-Lite
- Runtime: Ollama (runs inside Docker container)
- Purpose:
  - Daily / Weekly / Monthly performance analysis
  - Risk review and hypothesis generation (no trade commands)
  - Generates Markdown reports and summary text
- No API fees — all processing occurs locally.

### Automated Reporting System
1. Report Generation

    Periodic reports are automatically generated and stored under `/reports/YYYY-MM-DD/`.

| Report | Content | Trigger | Output |
|--------|-----------------|----------------|-------------------|
| Daily | Summary of PnL and trade count + LLM commentary | 23:55 UTC daily | `daily_summary.md`, graphs (PNG) |
| Weekly | Win/loss ratios by symbol + drawdown analysis + LLM insight | Every Sunday 23:57 UTC | `weekly_report.md`, PNG charts
| Monthly | KPI table + equity curve + LLM comprehensive review | 1st day of month 00:10 UTC | `monthly_report.md`, PNG heatmap

2. Visual Analytics

    All reports include:
    - **Performance Table**:  trades, win rate, net PnL, profit factor, max drawdown
    - **Equity Curve**: cumulative PnL graph
    - **Daily PnL Heatmap** – profit/loss by date
    - **PnL by Symbol** – top gainers and losers

Manual generation is also supported:
```bash
# Monthly report (auto-detects previous month)
python reports/report_cli.py --period monthly

# Specific date range
python reports/report_cli.py --from 2025-01-01 --to 2025-01-31
```

3. LLM-Based Analytics

    For each period, the LLM produces a natural-language analysis:

```bash
python reports/llm_analysis.py \
  --period weekly \
  --summary-json reports/2025-01-31/summary.json \
  --outdir reports/2025-01-31
```

4. GitHub Auto-Upload

    All reports (including Markdown and charts) can be automatically committed and pushed to a GitHub repository:

```bash
python reports/github_push.py --src reports/2025-01-31
```

> Configure your .env with:
> ```env
> GITHUB_REPO=https://<TOKEN>@github.com/<USER>/<REPO>.git
> GIT_AUTHOR_NAME=autobot
> GIT_AUTHOR_EMAIL=bot@yourdomain.tld
> ```

## Operational Notes
- **Binance API Key**: Disable withdrawal permissions, and use IP whitelisting if possible.
- **Logs/Backups**: Back up ./logs and data weekly.
- **Error Notifications**: Integrate with a Telegram bot for notifications (order execution, exceptions, LLM parsing failures).
- **Updates**: Parameter/strategy changes are limited to once a month; record the reason for the change and backtesting results.

## Local Setup
```bash
cd autotrade
# Configure keys and options
cp .env.example .env
# First run in paper-trading mode
# (set USE_PAPER=true)
docker compose up -d --build
docker logs -f autotrade-bot
```

## VPS Deployment
```bash
sudo apt update && sudo apt install -y docker.io docker-compose jq curl
sudo usermod -aG docker $USER && newgrp docker

git clone <repo> autotrade && cd autotrade
cp .env.example .env   # Key & Option setting

docker compose up -d --build
docker ps
docker logs -f autotrade-bot
```

## License
MIT License — Use freely for non-commercial and research purposes.
For commercial use, credit and compliance with exchange TOS are required.

