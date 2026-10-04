#!/bin/bash
# Unattended read-only weekly sync: headless Coach run, delivered to Discord via Hermes.
# Scheduled from cron on the VPS. Only read tools are allowed; see morning-prompt.md.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"

git pull --ff-only -q || echo "git pull failed; using local checkout" >&2

source scripts/readonly-tools.sh

out=$(timeout 600 claude -p "$(cat scripts/morning-prompt.md)" \
  --allowedTools "$ALLOWED" --permission-mode dontAsk 2>&1)
rc=$?

if [ $rc -ne 0 ]; then
  out="Coach morning sync failed (exit $rc). Last output: ${out: -400}"
elif [ "$(echo "$out" | tr -d '[:space:]')" = "[SILENT]" ]; then
  exit 0
fi

printf '%s' "$out" | docker exec -i hermes hermes send --to discord --subject "🚴 Coach" -f -
