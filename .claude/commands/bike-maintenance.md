---
description: Bike maintenance status — what's due/overdue, and log a service if reported
argument-hint: "[optional: 'did X' / 'serviced X on <date>' to log a completed service]"
---

Check bike maintenance status, and log any service the athlete reports.

1. **Load context.** Read `memory/bike-maintenance.md`. Pull the bike's current total
   odometer from the Strava MCP gear data (`get_gear`), matching on the Strava gear ID
   recorded in the file (confirm/update the ID if it's still marked TBD).

2. **If `$ARGUMENTS` reports a completed service** (e.g. "lubed the chain today", "shop
   did brakes and cables on the 10th"), update `memory/bike-maintenance.md` first:
   append a dated line to the Service log with today's date (or the stated date) and the
   current odometer, and update that item's "Last serviced" / "Odometer at last service"
   cells in the schedule table. Then continue to the status check below so the athlete
   sees the item drop off the due list.

3. **Compute status for every item** in the maintenance schedule: km since last service =
   current odometer − odometer at last service. Compare against the item's interval.
   Classify each as:
   - ✅ **OK** — well under interval
   - 🟡 **Due soon** — within ~15% of interval
   - 🔴 **Overdue** — past interval
   - ❓ **Unknown** — no service history recorded yet (don't guess; say so)

4. **Report:**

   ### 🔧 Maintenance status
   One line per item: status emoji, item, km since last service / interval, and a plain
   read (e.g. "🔴 Chain lube — 210 km since last lube (interval ~150–200 km) — overdue,
   lube before your next ride").

   ### 🗓️ Recommended this week
   Only the items that are due-soon or overdue, prioritized — call out anything genuinely
   safety-relevant (brakes) ahead of routine items (chain lube).

   If everything's unknown (no baseline yet), say so plainly and suggest logging current
   odometer + last known service dates as a starting baseline, rather than presenting
   fabricated due dates.

5. **Update memory.** If step 2 didn't already do it, still make sure any status changes
   (e.g. confirming the gear ID) are saved back to `memory/bike-maintenance.md`. Tell the
   user exactly what you updated.

Keep it tight — a status table plus a short recommendation, not an essay. Don't invent
odometer or service-date figures; if data is missing, say the check is limited.
