# AutoTradingProject

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

## Things to remember
- **Binance API Key**: Disable withdrawal permissions, and use IP whitelisting if possible.
- **Logs/Backups**: Back up ./logs and data weekly.
- **Error Notifications**: Integrate with a Telegram bot for notifications (order execution, exceptions, LLM parsing failures).
- **Updates**: Parameter/strategy changes are limited to once a month; record the reason for the change and backtesting results.