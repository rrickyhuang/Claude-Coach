---
description: List available ClaudeCoach slash commands
---

List the custom slash commands available in this project.

1. Read every `*.md` file in `.claude/commands/` (except this `help.md` itself), and pull
   each one's `description:` and `argument-hint:` frontmatter fields.
2. Present them as a list, one command per entry, sorted alphabetically by command name:
   `` /command-name [argument-hint] `` — description. If a command has no argument-hint,
   omit the bracket part.
3. Don't hardcode a command list from memory — always derive it by reading the files, so
   this stays accurate as commands are added, renamed, or removed.

Keep the output short — just the list, no extra commentary unless a command file is
missing a description (then note that instead of skipping it).
