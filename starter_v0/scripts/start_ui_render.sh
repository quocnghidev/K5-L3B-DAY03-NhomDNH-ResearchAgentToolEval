#!/usr/bin/env bash
# Start DNH chat UI on Render (or any PaaS that sets $PORT).
set -euo pipefail
cd "$(dirname "$0")/.."

PROVIDER="${UI_PROVIDER:-openrouter}"
MODEL="${UI_MODEL:-openai/gpt-4o-mini}"
VERSION="${UI_VERSION:-v3}"
HOST="${UI_HOST:-0.0.0.0}"
PORT="${PORT:-${UI_PORT:-8792}}"

exec python -m ui \
  --provider "$PROVIDER" \
  --model "$MODEL" \
  --version "$VERSION" \
  --host "$HOST" \
  --port "$PORT"
