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

---

## Analysis method & data gotchas (learned from prior sessions — apply these)

**Pull streams, not just summaries.** Get second-by-second `time, heart_rate, distance,
velocity_smooth, altitude, moving, temp` from the MCP. Units are metric — convert m/s →
km/h with ×3.6. Use `temp` when present to check heat as a drift factor.

**Aerobic decoupling — CONTROL FOR TERRAIN (the key gotcha).** Naive whole-ride
first-half/second-half speed-per-HR is *unreliable* on out-and-backs or when climbing is
front/back-loaded — it can flatter a net-downhill-home ride to near-zero and hide a real
drift (see the worked example in `memory/training-log.md`). Instead: compute grade from
altitude/distance, **filter to flat sections (|grade| < ~1–1.5%)**, and compare HR at
matched flat speed in the **first third vs final third of moving time**. Report drift in
bpm. Rising HR to hold the same flat pace = genuine drift. Use **moving time** (mask
speed > ~1.4 m/s), not elapsed, so stops don't distort bins.

**Efficiency trend:** avg_speed / avg_HR on comparable rolling terrain; rising = fitter.
Flag the temperature confound when temp data is missing/low.

**Data gotchas checklist:**
- **Discard implausible HR spikes as sensor glitches** (see `memory/athlete-profile.md`
  for known-bad values and the athlete's real max-HR range).
- End-of-long-ride max HR reads low (fatigue suppresses it) — don't treat as a new max.
- **No power meter** — never expect watts; HR only.
- Bulk-export timestamps are UTC → convert to America/Vancouver for any time-of-day logic
  (API `start_local` is already local).
- **HR zones are provisional** (estimated max, likely a touch high) until the LTHR field
  test lands — reason in RPE + the flat-ground ceiling too (see profile), not zones alone.

## Standing coaching points to reinforce
- Long rides: hold the ~140 bpm flat-ground ceiling early; let climbs go above. Praise Z2 discipline.
- Fuel ~60 g carbs/hr, small & frequent, from hour 1; no big solid meal right before a climb.
- Electrolytes the whole ride, ~500–750 ml/hr, sip every 15–20 min; weigh before/after, keep loss <2%.
- Track whether drift **onset moves later / shrinks** across the July–August long rides — that's the key progress signal.
- Protect the **Aug 15 dress rehearsal** above all other sessions.
