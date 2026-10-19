Unattended, READ-ONLY weekly sync (runs Sunday evening, planning the week ahead). Follow CLAUDE.md's "Daily sync floor" and "Commute-ride gap check", but you cannot and must not write anything: no calendar create/update/delete, no memory/ edits, no COROS workout changes. Propose changes in the message and say they need a live session to apply.

Steps:
1. Read memory/training-plan.md, memory/athlete-profile.md and memory/health-notes.md (recent entries).
2. List this week's and next week's Google Calendar events; diff the training events against training-plan.md and note any disagreement (calendar wins). Training events are `💪`-prefixed, plus legacy `🚴` events created before 2026-10-16 (see CLAUDE.md's calendar guardrails).
3. Quick COROS glance: queryRecoveryStatus, querySleepHrv, resting HR. Flag Low/Poor recovery or below-normal HRV using COROS's own labels, and say whether it should change the first sessions of the coming week.
4. Commute-ride gap check for the next 1-2 weeks, counting both `💪` and legacy `🚴` commute blocks; propose specific dates only.
5. Check the Strava activity list for everything since the newest entry in memory/training-log.md (not just yesterday) and list activities not yet logged.

Output: a short Discord message (under 1500 characters, plain text, no tables): the week ahead's planned sessions, any recovery flag, unlogged activities, and any proposed changes. If there are no flags, diffs, gaps or unlogged activities, output exactly [SILENT].
