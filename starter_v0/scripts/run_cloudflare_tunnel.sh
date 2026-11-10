#!/bin/zsh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
CF="$REPO/.tools/cloudflared"
PORT="${1:-8793}"
HOST="127.0.0.1"

# Cursor agent shells inject ALL_PROXY → breaks outbound LLM calls (chat → 502).
# Drop proxy env for UI + tunnel children; keep localhost NO_PROXY harmlessly.
unset ALL_PROXY HTTP_PROXY HTTPS_PROXY http_proxy https_proxy all_proxy || true
export NO_PROXY="127.0.0.1,::1,localhost,${NO_PROXY:-}"

if [[ ! -x "$CF" ]]; then
  echo "Missing $CF — downloading..."
  mkdir -p "$REPO/.tools"
  cd "$REPO/.tools"
  curl -fsSL -o cloudflared.tgz \
    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz"
  tar -xzf cloudflared.tgz
  chmod +x cloudflared
  CF="$REPO/.tools/cloudflared"
fi

# Ensure UI is up (DeepSeek preferred)
if ! lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Starting UI on $HOST:$PORT (deepseek, no proxy)..."
  cd "$ROOT"
  env -u ALL_PROXY -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy -u all_proxy \
    python3 -m ui --provider deepseek --version v3 --host "$HOST" --port "$PORT" &
  sleep 1.5
else
  # Warn if an already-running UI inherited a broken Cursor sandbox proxy.
  ui_pid="$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t 2>/dev/null | head -1 || true)"
  if [[ -n "${ui_pid}" ]] && ps eww -p "$ui_pid" 2>/dev/null | grep -q 'ALL_PROXY=http://127.0.0.1:'; then
    echo "WARN: UI pid $ui_pid on :$PORT still has ALL_PROXY (Cursor sandbox)."
    echo "      Chat will 502. Kill it and re-run this script, or start UI from Terminal.app."
  fi
fi

echo "Tunneling http://$HOST:$PORT ..."
echo "Copy the https://*.trycloudflare.com URL below into report A1."
exec "$CF" tunnel --url "http://$HOST:$PORT"
