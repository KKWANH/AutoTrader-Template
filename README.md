# Welcome to AutoTradingProject

> All investment decisions are the responsibility of the investor.


## Light weight project 
- Cheap hosting fee (Contabo VPS S)
- Open sourced LLM model
- Perform tasks based on programmed formulas
- Fast reaction speed

## High-profit, minimal-risk
- Whitelist-based universe control rules
    - **Market capitalization**: Top 50, Liquidity and price manipulation prevention
    - **Trading volume**: Over $50 million in 24-hour trading volume, minimal slippage
    - **Exchange reliability**: Tier 1 exchanges such as Binance/OKX, minimal listing/trading risk
    - **Project age**: Over 1 year since launch, minimal Rug Pull risk
    - **Major wallet distribution**: Top 10 wallets < 40% of total, preventing minority dominance
    - **On-chain activity**: Recent transactions on Etherscan/Explorer, ghost project filtering
    - **DeFi and meme coins**: “High Risk” tag, only separate strategies allowed, small amounts for volatility ranges
    - **Stablecoins, LP tokens, wrapped tokens, test tokens, and automated trading**: excluded, not suitable for this purpose

## Things to remember
- **Binance API Key**: Disable withdrawal permissions, and use IP whitelisting if possible.
- **Logs/Backups**: Back up ./logs and data weekly.
- **Error Notifications**: Integrate with a Telegram bot for notifications (order execution, exceptions, LLM parsing failures).
- **Updates**: Parameter/strategy changes are limited to once a month; record the reason for the change and backtesting results.

## How to run locally
```bash
cd autotrade

# Put key and options. Set USE_PAPER=true at first trial 
cp .env.example .env

docker compose up -d --build

docker logs -f autotrade-bot
```

## How to distribute on VPS(Contabo S)
```bash
sudo apt update && sudo apt install -y docker.io docker-compose jq curl

sudo usermod -aG docker $USER && newgrp docker

git clone <repo> autotrade && cd autotrade

cp .env.example .env   # Key & Option setting

docker compose up -d --build

docker ps

docker logs -f autotrade-bot
```