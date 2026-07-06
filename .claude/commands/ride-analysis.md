---
description: Structured post-activity analysis of the most recent (or specified) ride/hike
---

Run a consistent, structured analysis of a single activity. If the user named an
activity or date in `$ARGUMENTS`, use that; otherwise analyze their **most recent**
Strava activity.

Steps:

1. **Load context first.** Read `memory/athlete-profile.md` (zones, FTP, goals),
   `memory/training-plan.md` (what this week was *supposed* to be), and the top of
   `memory/training-log.md` (recent history). Then pull the activity from the Strava
   MCP — including HR, power, pace, elevation, and time-in-zone if available.

2. **Produce the analysis in exactly these sections:**

   ### 📊 Summary
   Distance, moving time, elevation, avg/normalized power, avg/max HR, TSS/effort,
   and how hard it actually was (with what metric tells you that).

   ### 🎯 vs. Plan
   What today was supposed to be per `training-plan.md`, and whether this hit it
   (on target / too easy / too hard / off-plan). Be honest.

   ### 🔍 What the data shows
   2–4 specific observations grounded in the numbers — pacing, zone distribution,
   cardiac drift / durability, climbing power, fade in the back half, fueling signs.

   ### 💪 What went well
   Genuine positives (only real ones).

   ### ⚠️ Watch / adjust
   Fatigue, overreaching, or execution issues — and whether recovery is needed.

   ### ✅ 2–3 concrete next steps
   Specific, actionable, tied to the plan and the Whistler goal.

3. **Update memory.** Append a dated entry to `memory/training-log.md` (newest at
   top), update `health-notes.md` / `training-plan.md` if warranted, and add a
   one-line note to `Status.md`. Tell the user exactly what you updated.

Keep it tight and specific. Cite the actual numbers you reasoned from. If the
activity lacks HR/power, say the analysis is limited rather than inventing figures.
