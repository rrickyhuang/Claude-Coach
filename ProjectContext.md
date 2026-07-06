# ProjectContext — Claude-Coach (GranFondoCoach)

Timeless reference for how the coaching system works. For current state and progress,
see [Status.md](Status.md) (gitignored). Contains no personal health data by design —
that all lives in `memory/` (gitignored).

## Purpose

A personal AI endurance coach built on **Claude Code + the official Strava MCP**.
Primary goal: train Ricky for the **RBC GranFondo Whistler (September)** — a ~122 km
Sea-to-Sky ride with sustained climbing — and support general health. It turns the
Strava MCP (a read-only data pipe) into an actual coaching system by adding persistent
memory, a consistent structured-analysis workflow, and a defined coaching method.

## Why this over a plain chat / Chat Project

The Strava MCP alone has three coaching gaps (widely noted in reviews): its memory is
only a per-conversation summary, it has no consistent method, and it tends to agree
with the user. This project closes all three:

- **Memory** → `memory/` files Claude reads *and writes* each session, so state compounds.
- **Consistency** → `/ride-analysis` + `/weekly-review` run fixed templates every time.
- **Method** → `CLAUDE.md` encodes a real periodized philosophy + "hold me accountable."

## How it works

1. The **Strava MCP** (read-only, OAuth, needs a Strava subscription) supplies live
   activity data — HR, power, pace, GPS, fitness/readiness/load trends, gear.
2. **`CLAUDE.md`** defines the coaching method, tone, safety rules, and the standing
   instruction to update memory after every session.
3. **Slash commands** (`.claude/commands/`) run structured, repeatable analyses.
4. **`memory/`** holds the context Strava doesn't: profile/zones, the periodized plan,
   a running training log, and health notes. Coach updates these each session.
5. The **Google Calendar MCP** provides two-way schedule sync: the actual training
   sessions live as `🚴` calendar events (alongside Ricky's fixed commitments). The coach
   reads the live schedule when planning and writes plan changes back — guardrailed to
   only ever touch training events, and to confirm before deletes/big moves.

## Key files

- `CLAUDE.md` — coaching method, tone, safety, memory-update rules (the system's brain)
- `.claude/commands/ride-analysis.md` — `/ride-analysis`: structured post-activity breakdown
- `.claude/commands/weekly-review.md` — `/weekly-review`: weekly progress vs. plan + next week
- `memory/athlete-profile.md` — durable facts: zones, FTP, history, goals, constraints
- `memory/training-plan.md` — living periodized plan → Whistler
- `memory/training-log.md` — dated per-activity + weekly entries (newest at top)
- `memory/health-notes.md` — sleep/fatigue/injury/nutrition/readiness signals
- `memory/*.example.md` — committed templates for each of the above
- `Status.md` — dated progress notes (gitignored)

## Commands

```
/ride-analysis [activity or date]   # structured breakdown of one activity (defaults to most recent)
/weekly-review [week]               # weekly progress vs. plan + next week (defaults to last 7 days)
```

Strava MCP setup:
```
claude mcp add --transport http strava-mcp https://mcp.strava.com/mcp
```

## Settled decisions

- **Strava MCP is read-only.** Nothing is written back to Strava or pushed to a device;
  all coaching output lives in this repo's memory files.
- **Google Calendar is the schedule's source of truth, synced two-way.** Training
  sessions are `🚴`-prefixed events; `memory/training-plan.md` mirrors them + holds
  rationale. The coach may read the whole calendar (to plan around commitments) but only
  ever *writes* to `🚴` training events, and confirms before deletes or big moves.
- **Personal data is gitignored.** Everything in `memory/` (except `*.example.md`) plus
  `Status.md` stays private; the repo is safe to make public.
- **Memory is the differentiator.** The standing rule in `CLAUDE.md` — update the log/
  plan/health/status files every session — is what makes this more than a stateless chat.
- **Coach is deliberately non-sycophantic.** The method mandates honest pushback and
  prescribing recovery against the athlete's wishes when the data warrants.
- **Periodized toward one A-event** (Whistler, September): base → build → peak → taper.

## Not yet built

- **Automated scheduled summary emails.** Planned: a recurring job (weekly-ish) that runs
  a `/weekly-review`-style analysis and emails a concise summary + advice to Ricky's
  Gmail, so updates arrive without him prompting. See Status.md open items for design notes.

## Repo

GitHub: https://github.com/rrickyhuang/Claude-Coach — personal health data gitignored.
