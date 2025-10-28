#!/usr/bin/env bash
set -e

# Wait for ollama to be ready
bash scripts/wait-for-http.sh http://ollama:11434/api/tags 120

# Preload required models (lightweight recommendation: phi3:mini)
if ! curl -sf http://ollama:11434/api/tags | jq -r '.models[].name' | grep -q '^phi3:mini$'; then
  echo "[init] pulling phi3:mini ..."
  curl -s -X POST http://ollama:11434/api/pull -d '{"name":"phi3:mini"}' >/dev/null
fi

echo "[init] ollama models ready."
