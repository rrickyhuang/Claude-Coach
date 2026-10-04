# Sourced by the unattended scripts. Read-only tools only: no calendar, memory or COROS writes.
C=mcp__claude_ai_COROS__
S=mcp__claude_ai_Strava__
G=mcp__claude_ai_Google_Calendar__
ALLOWED="Read,Glob,Grep,${G}list_events,${G}search_events,${G}get_event,${G}list_calendars,${S}list_activities,${S}get_activity_performance,${S}get_athlete_profile,${C}queryRecoveryStatus,${C}querySleepHrv,${C}querySleepOverview,${C}queryRestingHeartRate,${C}queryStressLevel,${C}queryTrainingLoadAssessment,${C}queryDailyHealthData"
