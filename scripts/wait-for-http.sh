#!/usr/bin/env bash
# Usage: wait-for-http.sh http://localhost:11434/api/tags 60

URL="${1:-http://localhost:11434/api/tags}"
TIMEOUT="${2:-60}"
for i in $(seq 1 $TIMEOUT); do
  if curl -sf "$URL" >/dev/null 2>&1; then
    exit 0
  fi
  sleep 1
done
echo "Timeout waiting for $URL"
exit 1
