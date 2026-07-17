---
description: Structured post-activity analysis of the most recent (or specified) ride/hike
argument-hint: "[activity name/date] [-- how it felt, struggles, questions, food/hydration notes]"
---

Run a consistent, structured analysis of a single activity. Parse `$ARGUMENTS` for two
independent, optional parts:
- **Which activity** — a name, date, or description. Default to the **most recent**
  Strava activity if none is given.
- **Subjective notes from the athlete** — how it felt, where they struggled, specific
  questions they want answered, or food/hydration details (e.g. what/when they ate or
  drank, GI issues, cramping, bonking). This can be free text anywhere in `$ARGUMENTS` —
  it doesn't need a special delimiter, just read the intent. If present, treat it as
  first-class input to weigh alongside the Strava data, not an aside.

Steps:

1. **Load context first.** Read `memory/goals.md` (what the athlete is training toward),
   `memory/athlete-profile.md` (zones, FTP), `memory/training-plan.md` (what this week
   was *supposed* to be), and the top of `memory/training-log.md` (recent history). Then
   pull the activity from the Strava MCP — including HR, power, pace, elevation, and
   time-in-zone if available. Also pull COROS recovery status (`queryRecoveryStatus`) and
   sleep data (`querySleepData`) from around the time of the activity, to contextualize how
   the ride felt against how recovered the athlete actually was. Activity data itself
   stays Strava-primary — only fall back to COROS activity data (`querySportRecords`,
   `getActivityDetail`, `downloadActivityFitFiles`) when Strava doesn't have the activity
   at all.

2. **Produce the analysis in exactly these sections:**

   ### 📊 Summary
   Distance, moving time, elevation, avg/normalized power, avg/max HR, TSS/effort,
   and how hard it actually was (with what metric tells you that).

   ### 🎯 vs. Plan
   What today was supposed to be per `training-plan.md`, and whether this hit it
   (on target / too easy / too hard / off-plan). Be honest.

   ### 🔍 What the data shows
   2–4 specific observations grounded in the numbers — pacing, zone distribution,
   cardiac drift / durability, climbing power, fade in the back half, fueling signs. Fold
   in COROS recovery/sleep context when it's relevant to explaining the numbers, e.g.
   "power was down 8% but recovery was only 40% going in."

   ### 🗣️ Athlete report
   Only include this section if the athlete gave subjective notes. Reconcile what they
   said (how it felt, where they struggled, food/hydration specifics) against what the
   data shows — confirm it, add nuance, or gently push back if the data tells a different
   story (e.g. legs "felt fine" but HR drift says otherwise). Directly answer any
   questions they asked.

   ### 💪 What went well
   Genuine positives (only real ones).

   ### ⚠️ Watch / adjust
   Fatigue, overreaching, or execution issues — and whether recovery is needed. Fold in
   any struggle points or fueling issues the athlete reported.

   ### 🧘 Stretch & roll
   A short (~10 min) post-ride recommendation, tailored to what *this* ride stressed —
   see the stretching/mobility protocol in `memory/health-notes.md` (priority areas:
   quads, hip flexors, calves — they double as support for the descent-pain/eccentric-
   load niggle in `athlete-profile.md`). Climbing-heavy ride → quads/hip flexors/calves;
   hard interval day → calves/glutes; long saddle time → hip flexors/lower back. If the
   *next* session on `training-plan.md` is a hard/interval day, also suggest a specific
   dynamic warm-up (leg swings, walking lunges, hip circles, easy spin-up) rather than
   going in cold.

   ### ✅ 2–3 concrete next steps
   Specific, actionable, tied to the plan and the goal(s) in `memory/goals.md`.

   ### 🔧 Maintenance check
   Only include this section if `memory/bike-maintenance.md` shows an item newly
   due-soon or overdue once this ride's distance is added to the bike's odometer (pull
   current odometer from the Strava MCP gear data). One line, e.g. "Chain's at ~210 km
   since last lube — due for a relube." Skip the section entirely if nothing's due; don't
   run the full `/bike-maintenance` report here.

3. **Update memory.** Append a dated entry to `memory/training-log.md` (newest at
   top) — include the athlete's subjective notes verbatim or lightly summarized, not
   just the numbers. Update `health-notes.md` (e.g. new fueling issue, injury signal,
   fatigue pattern) / `training-plan.md` if warranted. Tell the user exactly what you
   updated.

Keep it tight and specific. Cite the actual numbers you reasoned from. If the
activity lacks HR/power, say the analysis is limited rather than inventing figures.

---

## Analysis method & data gotchas (learned from prior sessions — apply these)

**Pull streams, not just summaries.** Get second-by-second `time, heart_rate, distance,
velocity_smooth, altitude, moving, temp` from the MCP. Units are metric — convert m/s →
km/h with ×3.6. Use `temp` when present to check heat as a drift factor.

**Aerobic decoupling — CONTROL FOR TERRAIN (the key gotcha).** Naive whole-ride
first-half/second-half speed-per-HR is *unreliable* on out-and-backs or when climbing is
front/back-loaded — it can flatter a net-downhill-home ride to near-zero and hide a real
drift (see the worked example in `memory/training-log.md`, if your log has one yet).
Instead: compute grade from
altitude/distance, **filter to flat sections (|grade| < ~1–1.5%)**, and compare HR at
matched flat speed in the **first third vs final third of moving time**. Report drift in
bpm. Rising HR to hold the same flat pace = genuine drift. Use **moving time** (mask
speed > ~1.4 m/s), not elapsed, so stops don't distort bins.

**Efficiency trend:** avg_speed / avg_HR on comparable rolling terrain; rising = fitter.
Flag the temperature confound when temp data is missing/low.

**Data gotchas checklist:**
- **Discard implausible HR spikes as sensor glitches** (see `memory/athlete-profile.md`
  for known-bad values and the athlete's real max-HR range).
- End-of-long-ride max HR reads low — treat it as fatigue-suppressed, not a new max.
- **No power meter** — reason from HR only.
- Bulk-export timestamps are UTC → convert to America/Vancouver for any time-of-day logic
  (API `start_local` is already local).
- **HR zones are provisional** (estimated max, likely a touch high) until the LTHR field
  test lands — reason in RPE + the flat-ground ceiling too (see profile), not zones alone.
- **Check lap distances before calling laps auto-generated or manual.** Near-uniform
  distances (e.g. every 1 km/1 mi) mean auto-lap; irregular distances mean the athlete
  pressed the lap button manually (e.g. to mark interval reps). State which one it is,
  based on the distances, rather than assuming.
- **Cross-check the conversation before assigning a cause to a data anomaly**
  (elapsed-vs-moving gaps, HR spikes during "recovery," etc.). If the athlete already
  mentioned a stop, food break, mechanical, or traffic light earlier in the session,
  that's ground truth — use it instead of guessing a plausible-sounding story from the
  numbers alone.
- **Label inferred causes as inferred, not confirmed.** A specific explanation for a
  data blip (e.g. "that HR spike was a hard reaccel out of a stop") is a hypothesis
  unless the raw stream or the athlete confirms it — say "likely"/"possibly," or ask,
  rather than stating it as fact.

## Standing coaching points to reinforce
- Long rides: hold the athlete's flat-ground HR ceiling early (see `memory/athlete-profile.md`); let climbs go above. Praise Z2 discipline.
- Fuel ~60 g carbs/hr, small & frequent, from hour 1; no big solid meal right before a climb.
- Electrolytes the whole ride, ~500–750 ml/hr, sip every 15–20 min; weigh before/after, keep loss <2%.
- Track whether drift **onset moves later / shrinks** across upcoming long rides — that's the key progress signal.
- Protect whatever session `memory/training-plan.md` flags as the key dress-rehearsal/peak ride above all others.
