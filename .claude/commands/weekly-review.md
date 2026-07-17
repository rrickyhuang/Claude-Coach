---
description: Weekly training review — progress vs. plan and next week's focus
argument-hint: "[week description, e.g. 'last week' or a date range — omit for last 7 days]"
---

Run a weekly review. If `$ARGUMENTS` names a week, use it; otherwise review the
**last 7 days**.

1. **Load context.** Read `memory/goals.md`, `memory/training-plan.md`,
   `memory/training-log.md`, and `memory/health-notes.md`. Pull the week's activities and
   fitness/freshness/readiness trends from the Strava MCP. Also pull the week's COROS
   trend data — average and resting heart rate (`queryAvgHeartRate`,
   `queryRestingHeartRate`), sleep (`querySleepData`), stress (`queryStressLevel`), and
   training load assessment (`queryTrainingLoadAssessment`) — alongside the Strava
   fitness/freshness pull. **Also read the upcoming 1–2 weeks from Google Calendar** (the
   live schedule + fixed commitments) — prefer it over memory if they disagree, and
   reconcile.

2. **Produce the review in these sections:**

   ### 📅 Week in numbers
   Total hours, distance, elevation, TSS/load, number of sessions, and the
   intensity distribution (easy vs. hard). Compare to what the plan called for.

   ### 📈 Fitness trend
   Direction of CTL/fitness, ATL/fatigue, and form/freshness. Are we building,
   holding, or digging a hole? Fold in the COROS recovery/HRV/sleep/stress trend
   alongside CTL/ATL/form — e.g. rising fatigue paired with declining recovery or
   below-normal HRV strengthens the read; recovering HRV against a big training week
   is a good sign. If there's a dated A goal in `memory/goals.md`, how many weeks
   remain and are we on track?

   ### ✅ Wins / ⚠️ Concerns
   Honest read — consistency, key sessions hit or missed, fatigue/health flags.

   ### 🗓️ Next week
   A concrete week plan (session-by-session focus, not just totals), shaped by the
   current goal(s) in `memory/goals.md` (periodized toward a dated event, or the current
   focus block for an ongoing goal), adjusted for how this week actually went and current
   fatigue. Apply CLAUDE.md's commute-ride gap-check and commute/hard-session folding
   rules to the upcoming 1–2 weeks — this review is one of its two triggers (the daily
   sync is the other).

   ### 🔧 Maintenance check
   Only include this section if `memory/bike-maintenance.md` shows anything due-soon or
   overdue (compare current Strava gear odometer against each item's interval). List just
   the due items; suggest `/bike-maintenance` for the full picture. Skip the section if
   nothing's due.

3. **Update memory + calendar.** Update `memory/training-plan.md` to reflect the next
   week and any shift, and add a dated summary to `memory/training-log.md`. If the plan
   for next week changed, **write it back to Google Calendar**, following the calendar
   guardrails in CLAUDE.md. Tell the user exactly what you changed in both memory and
   the calendar.

Be direct about whether the athlete is on track for their target event. If recovery is
needed, prescribe it even if a bigger week was planned.
