FROM python:3.11-slim

WORKDIR /app

# System util
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates bash jq && \
    rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source
COPY . .

# Log directory
RUN mkdir -p /app/logs

# Default command is specified in compose
