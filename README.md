# ClaudeCoach

A personal AI cycling/endurance coach built on **Claude + the official Strava MCP**.
Goal-agnostic: works for a target event, an ongoing fitness/health goal, or several
goals at once — see `memory/goals.md`.

The Strava MCP is a great *data pipe* but not, on its own, a coach: its memory is just
a per-conversation summary, it has no consistent method, and it tends to agree with you.
This project fixes that by wrapping it in four things Claude Code makes real:

1. **Persistent memory** — `memory/` files Claude reads *and updates* after every session,
   so training state compounds instead of evaporating between chats.
2. **Structured commands** — `/ride-analysis` and `/weekly-review` run the *same*
   analysis template every time, so feedback is consistent, not improvised.
3. **A defined method** — `CLAUDE.md` encodes a real coaching philosophy (periodization
   toward a dated goal, rolling focus blocks for ongoing goals, when to push vs. recover)
   and tells Claude to hold you accountable rather than just validate you.
4. **Two-way Google Calendar sync** — the actual training plan lives as `🚴`-prefixed
   calendar events alongside your real commitments. Claude reads the live schedule when
   planning and writes changes back, guardrailed to only ever touch training events and
   to confirm before deletes or big moves (see `CLAUDE.md`'s "Calendar sync" section).

## How it works

1. The **Strava MCP** (read-only, OAuth, needs a Strava subscription) supplies live
   activity data — HR, power, pace, GPS, fitness/readiness trends, gear.
2. **`CLAUDE.md`** defines the coaching method, tone, safety rules, calendar-sync
   guardrails, and the standing instruction to update memory after every session.
3. **Slash commands** (`.claude/commands/`) run structured, repeatable analyses.
4. **`memory/`** holds context Strava doesn't: what you're training toward (goals),
   profile/zones, the periodized plan, a running training log, and health notes. Coach
   updates these each session.
5. The **Google Calendar MCP** provides the live schedule and is written back to when
   the plan shifts.

## Setup

1. **Connect the Strava MCP** (read-only, needs a Strava subscription):
   ```
   claude mcp add --transport http strava-mcp https://mcp.strava.com/mcp
   ```
   Then authorize via the OAuth browser prompt. (On claude.ai/Cowork instead:
   Customize → Connectors → search "Strava" → Connect.)
2. **Fill in your memory files.** Copy each `memory/*.example.md` to the same name
   without `.example` and fill it in (these real files are gitignored). On macOS/Linux
   use `cp`; on Windows PowerShell use `Copy-Item`:
   ```
   cp memory/goals.example.md          memory/goals.md
   cp memory/athlete-profile.example.md memory/athlete-profile.md
   cp memory/training-plan.example.md  memory/training-plan.md
   cp memory/training-log.example.md   memory/training-log.md
   cp memory/health-notes.example.md   memory/health-notes.md
   ```
3. **Start coaching.** After a ride or hike:
   ```
   /ride-analysis            # structured post-activity breakdown
   /weekly-review            # progress vs. plan + next week's focus
   ```

## Key files

- `CLAUDE.md` — coaching method, tone, safety, calendar-sync guardrails, memory-update
  rules (the system's brain)
- `.claude/commands/ride-analysis.md` — `/ride-analysis`: structured post-activity breakdown
- `.claude/commands/weekly-review.md` — `/weekly-review`: weekly progress vs. plan + next week
- `memory/goals.md` — what you're training toward: target event(s), non-event goals,
  constraints (source of truth for goal state)
- `memory/athlete-profile.md` — durable facts: zones, physiology, history
- `memory/training-plan.md` — living plan toward the current goal(s)
- `memory/training-log.md` — dated per-activity + weekly entries (newest at top)
- `memory/health-notes.md` — sleep/fatigue/injury/nutrition/readiness signals
- `memory/*.example.md` — committed templates for each of the above
- Open tasks/ideas are tracked as [GitHub Issues](https://github.com/rrickyhuang/Claude-Coach/issues)

## Settled decisions

- **Strava MCP is read-only.** Nothing is written back to Strava or pushed to a device;
  all coaching output lives in this repo's memory files.
- **Google Calendar is the schedule's source of truth, synced two-way.** Training
  sessions are `🚴`-prefixed events; `memory/training-plan.md` mirrors them + holds
  rationale. The coach may read the whole calendar (to plan around commitments) but only
  ever *writes* to `🚴` training events, and confirms before deletes or big moves.
- **Personal data is gitignored.** Everything in `memory/` (except `*.example.md`) stays
  private; the repo is safe to make public.
- **Memory is the differentiator.** The standing rule in `CLAUDE.md` — update the log/
  plan/health files every session — is what makes this more than a stateless chat.
- **Coach is deliberately non-sycophantic.** The method mandates honest pushback and
  prescribing recovery against the athlete's wishes when the data warrants.
- **Goal-agnostic periodization.** `memory/goals.md` drives it: a dated A-goal gets
  base → build → peak → taper; ongoing/non-event goals get rolling focus blocks instead.
  Multiple goals are prioritized (A goal's calendar wins) rather than assumed away.

## What's tracked vs. private

- **Tracked (safe to push):** this README, `CLAUDE.md`, the `.claude/commands/`, and
  the `memory/*.example.md` templates.
- **Gitignored (private):** everything in `memory/` (real health/training data) and any
  secrets. See `.gitignore`.

## Limitations (inherent to the Strava MCP)

- **Read-only** — advice lives in your files; nothing is pushed to your device/calendar.
- **Not proactive** — you initiate each session; it won't message you first.
- Analysis is only as good as your recorded data (make sure rides capture HR/power).

## Not yet built

- **Automated scheduled summary emails** — a recurring job that runs a
  `/weekly-review`-style analysis and emails a concise summary + advice, so updates
  arrive without prompting. See the [Issues](https://github.com/rrickyhuang/Claude-Coach/issues).
