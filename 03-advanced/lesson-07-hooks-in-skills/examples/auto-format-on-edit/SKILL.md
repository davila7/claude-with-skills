---
name: auto-format-on-edit
description: Automatically format code files after every edit using Prettier and ESLint. Active in the background whenever Claude edits a file. Formatting is silent — no prompts, no output unless a formatter fails. Use when you want consistent formatting enforced automatically during a coding session.
user-invocable: false
allowed-tools: Bash(npx prettier *) Bash(npx eslint *)
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/scripts/format.sh"
---

Formatting is applied automatically after every file edit via the PostToolUse hook defined in this skill's frontmatter. You do not need to run any formatter manually.

## What happens after each edit

When Claude uses the Edit or Write tool on any file, the PostToolUse hook fires and runs `scripts/format.sh`. That script:

1. Reads the edited file path from the hook input JSON
2. Checks whether the file has a recognized extension (.js, .ts, .jsx, .tsx, .css, .json, .md)
3. Runs `npx prettier --write` on the file if Prettier is available
4. Runs `npx eslint --fix` on the file if ESLint is available and the file is a script type (.js, .ts, .jsx, .tsx)
5. Exits 0 regardless of outcome — formatting failures are never allowed to block edits

## What is not formatted

- Binary files
- Files outside recognized extensions
- Files in node_modules, dist, .git, or similar directories
- Files where the formatter is not installed

## If the user asks why files look different after editing

Explain that `auto-format-on-edit` is active. It runs Prettier and ESLint after each edit to enforce consistent formatting. To disable it, remove or deactivate this skill.

## If a formatter produces unexpected results

Ask the user to check their `.prettierrc` or `.eslintrc` configuration files. The skill runs formatters with whatever project-level configuration is present — it does not override formatter settings.
