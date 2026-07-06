# TODO

Open tasks and ideas for this project. Public-safe — no personal health/training
numbers here (those live in the gitignored `memory/` files). See `git log` for history
of what's already shipped.

- [ ] Complete Strava MCP OAuth authorization (registered at user scope; needs the
      browser auth step + a session restart to load its tools)
- [ ] Complete Google Calendar MCP connection at user scope in project sessions (mirrors
      the Strava setup) so two-way calendar sync works from Claude Code
- [ ] Run a lactate-threshold field test and rebuild HR zones off the result (current
      zones are provisional on an estimated max) — see `memory/athlete-profile.md`
- [ ] Track cardiac-drift trend across upcoming long rides — a key fitness signal
      once analysis is running (method documented in `.claude/commands/ride-analysis.md`)
- [ ] Log fluid/electrolyte/carb intake on long rides so fuel/hydration can be tuned
      against measured drift
- [ ] Run a first real `/ride-analysis` on a recent ride to pressure-test the workflow
- [ ] Design and build automated scheduled summary/progress reports emailed via Gmail —
      needs a scheduling mechanism, Gmail-send capability, and a concise email template
      distinct from the full in-chat review (see README's "Not yet built")
- [ ] Watch for training-plan disruption around any planned travel gaps; protect key
      long rides before/after them
