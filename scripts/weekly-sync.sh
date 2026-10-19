#!/bin/bash
# Unattended read-only weekly sync: headless Coach run, delivered to Discord via Hermes.
# Scheduled from cron on the VPS (stdout/stderr go to weekly-sync.log). Only read tools are
# allowed; see weekly-prompt.md and readonly-tools.sh.
#
# Everything lives in main() and the script exits right after calling it, so bash has
# parsed the whole body before the git pull below can rewrite this file mid-run.
main() {
  set -uo pipefail
  cd "$(dirname "$0")/.." || exit 1
  export PATH="$HOME/.local/bin:$PATH"

  branch=$(git branch --show-current)
  if [ "$branch" = main ]; then
    git pull --ff-only -q || echo "git pull failed; using local checkout" >&2
  else
    echo "checkout is on '$branch', not main; skipping git pull" >&2
  fi

  source scripts/readonly-tools.sh

  # stdout only: stderr (warnings, MCP auth notices) goes to the log, not to Discord.
  out=$(timeout 600 claude -p "$(cat scripts/weekly-prompt.md)" \
    --allowedTools "$ALLOWED" --disallowedTools "$DENIED" --permission-mode dontAsk)
  rc=$?

  if [ $rc -ne 0 ]; then
    echo "claude exited $rc" >&2
    out="Coach weekly sync failed (exit $rc). See ~/Claude-Coach/weekly-sync.log on the VPS."
  elif [ "$(echo "$out" | tr -d '[:space:]')" = "[SILENT]" ]; then
    return 0
  fi

  # Discord rejects messages over 2000 characters; leave room for the subject line.
  if ! printf '%s' "${out:0:1900}" | docker exec -i hermes hermes send --to discord --subject "💪 Coach" -f -; then
    echo "hermes send failed; the summary was not delivered" >&2
    return 1
  fi
}

main "$@"
exit $?
