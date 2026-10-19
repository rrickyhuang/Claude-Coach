# Sourced by the unattended scripts. Read-only tools only: no calendar, memory or COROS writes.
# File reads are limited to this repo, and secrets locations are explicitly denied, because the
# run reads untrusted text (calendar and Strava descriptions) that could try to prompt-inject it.
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
C=mcp__claude_ai_COROS__
S=mcp__claude_ai_Strava__
G=mcp__claude_ai_Google_Calendar__
ALLOWED="Read(/${REPO}/**),${G}list_events,${G}search_events,${G}get_event,${G}list_calendars,${S}list_activities,${S}get_activity_performance,${S}get_athlete_profile,${C}queryRecoveryStatus,${C}querySleepHrv,${C}querySleepOverview,${C}queryRestingHeartRate,${C}queryStressLevel,${C}queryTrainingLoadAssessment,${C}queryDailyHealthData"
DENIED="Read(~/.hermes/**),Read(~/.claude/**),Read(~/.claude.json),Read(~/.ssh/**),Read(~/.git-credentials),Read(~/.config/**),Read(~/.local/**),Read(~/.npm/**),Read(//etc/**),Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch"
