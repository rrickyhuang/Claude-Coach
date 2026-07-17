---
description: Deep-dive readiness check — COROS recovery, HRV, sleep, stress, and training load
argument-hint: "[optional: a specific date/day to check instead of today]"
---

Run a full COROS wellness deep-dive on demand. This is the heavier counterpart to the
daily sync's lightweight glance (a quick recovery/resting-HR/sleep-score check CLAUDE.md
already runs at the start of each new calendar day) — use `/readiness` when the athlete
wants the complete picture rather than just the headline flag.

1. **Load context first.** Read `memory/goals.md` and `memory/training-plan.md` (what
   today or the next session is supposed to be), and the top of `memory/health-notes.md`
   (recent signals, ongoing niggles). Then pull from the COROS MCP:
   - Recovery status (`queryRecoveryStatus`)
   - Sleep HRV assessment vs. baseline (`querySleepHrv`)
   - Sleep data/architecture (`querySleepData`)
   - Stress trend (`queryStressLevel`)
   - Training load assessment (`queryTrainingLoadAssessment`)
   - Fitness assessment overview (`queryFitnessAssessmentOverview`), if relevant to the
     question at hand

2. **Produce the report in these sections:**

   ### 🔋 Recovery status
   Current recovery level (COROS's own categorical label, e.g. Low/Adequate/High) and
   what it implies for today's planned intensity.

   ### 💤 Sleep & HRV
   Sleep score, duration, architecture (deep/REM/light if available), and HRV vs. the
   athlete's baseline — call out whether HRV reads in/below/above normal range using
   COROS's own evaluation, not an invented numeric cutoff.

   ### 😮‍💨 Stress trend
   Recent stress level trend and whether it's elevated relative to the athlete's norm.

   ### 📊 Training load
   COROS's training load assessment (ratio/status), and — if pulled — how the fitness
   assessment overview fits with where `memory/training-plan.md` says the athlete should
   be right now.

   ### 🎯 What this means for today
   A direct, practical read: proceed as planned, modify (specify how — reduce intensity,
   swap to easy, or rest), or flag to a medical professional if something looks like a
   red flag rather than a training signal. Tie it to what's actually on `training-plan.md`
   or the calendar for today, if known.

3. **If anything looks off** (recovery Low/Poor, HRV below normal range, stress notably
   elevated), say so plainly and suggest a concrete adjustment — but don't touch the
   calendar without asking first, per CLAUDE.md's calendar guardrails.

Keep it tight — a short report per section, not an essay. If a COROS metric isn't
available, say the picture is limited rather than inventing numbers.
