# GranFondoCoach

A personal AI cycling/endurance coach built on **Claude + the official Strava MCP**,
aimed at training for the **RBC GranFondo Whistler** (September) and general health.

The Strava MCP is a great *data pipe* but not, on its own, a coach: its memory is just
a per-conversation summary, it has no consistent method, and it tends to agree with you.
This project fixes that by wrapping it in three things Claude Code makes real:

1. **Persistent memory** — `memory/` files Claude reads *and updates* after every session,
   so training state compounds instead of evaporating between chats.
2. **Structured commands** — `/ride-analysis` and `/weekly-review` run the *same*
   analysis template every time, so feedback is consistent, not improvised.
3. **A defined method** — `CLAUDE.md` encodes a real coaching philosophy (periodization
   toward the Fondo, when to push vs. recover) and tells Claude to hold you accountable
   rather than just validate you.

## Setup

1. **Connect the Strava MCP** (read-only, needs a Strava subscription):
   ```
   claude mcp add --transport http strava-mcp https://mcp.strava.com/mcp
   ```
   Then authorize via the OAuth browser prompt. (On claude.ai/Cowork instead:
   Customize → Connectors → search "Strava" → Connect.)
2. **Fill in your memory files.** Copy each `memory/*.example.md` to the same name
   without `.example` and fill it in (these real files are gitignored):
   ```
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

## What's tracked vs. private

- **Tracked (safe to push):** this README, `CLAUDE.md`, `ProjectContext.md`,
  the `.claude/commands/`, and the `memory/*.example.md` templates.
- **Gitignored (private):** everything in `memory/` (real health/training data),
  `Status.md`, and any secrets. See `.gitignore`.

## Limitations (inherent to the Strava MCP)

- **Read-only** — advice lives in your files; nothing is pushed to your device/calendar.
- **Not proactive** — you initiate each session; it won't message you first.
- Analysis is only as good as your recorded data (make sure rides capture HR/power).
