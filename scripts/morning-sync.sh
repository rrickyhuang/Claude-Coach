#!/bin/bash
# Unattended read-only weekly sync: headless Coach run, delivered to Discord via Hermes.
# Scheduled from cron on the VPS. Only read tools are allowed; see morning-prompt.md.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"

git pull --ff-only -q || echo "git pull failed; using local checkout" >&2

C=mcp__claude_ai_COROS__
S=mcp__claude_ai_Strava__
G=mcp__claude_ai_Google_Calendar__
ALLOWED="Read,Glob,Grep,${G}list_events,${G}search_events,${G}get_event,${G}list_calendars,${S}list_activities,${S}get_activity_performance,${S}get_athlete_profile,${C}queryRecoveryStatus,${C}querySleepHrv,${C}querySleepOverview,${C}queryRestingHeartRate,${C}queryStressLevel,${C}queryTrainingLoadAssessment,${C}queryDailyHealthData"

out=$(timeout 600 claude -p "$(cat scripts/morning-prompt.md)" \
  --allowedTools "$ALLOWED" --permission-mode dontAsk 2>&1)
rc=$?

if [ $rc -ne 0 ]; then
  out="Coach morning sync failed (exit $rc). Last output: ${out: -400}"
elif [ "$(echo "$out" | tr -d '[:space:]')" = "[SILENT]" ]; then
  exit 0
fi

printf '%s' "$out" | docker exec -i hermes hermes send --to discord --subject "🚴 Coach" -f -
