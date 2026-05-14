# claude-with-skills

A progressive course teaching Agent Skills for Claude Code, from anatomy to advanced orchestration patterns.

## Repository layout

```
00-introduction/          # Conceptual foundation (what skills are, how they load)
01-basic/                 # Anatomy, scopes, repetitive tasks, documentation, invocation
02-intermediate/          # Full frontmatter reference, arguments, dynamic context, combining options
03-advanced/              # Forked context, subagent wiring, orchestration, hooks, plugins, capstone
reference/                # Cheatsheets: frontmatter, substitutions, invocation matrix, headless, troubleshooting
scripts/                  # install-examples.sh — copies a skill directory into personal or project scope
```

Each numbered section contains:
- `README.md` — learning objectives and lesson index
- `lesson-NN-<topic>/README.md` — concept explanation
- `lesson-NN-<topic>/examples/<skill-name>/SKILL.md` — runnable skill
- `exercises/` — prompts with `solutions/` subdirectory

## SKILL.md conventions

Every `SKILL.md` must have valid YAML frontmatter:

```yaml
---
name: skill-name          # lowercase, hyphens only, max 64 chars, matches directory name
description: ...          # plain text, max 1024 chars, written for the model not for humans
---
```

- Names: lowercase letters, digits, hyphens only. No underscores.
- Descriptions: written so Claude can decide at startup whether to activate the skill — not marketing copy.
- Body: keep under 500 lines / 5000 tokens. Move reference material to `references/` subdirectories.
- Claude Code-specific fields (`disable-model-invocation`, `user-invocable`, `argument-hint`, `arguments`, `paths`, `shell`, `context`, `agent`, `hooks`, `model`, `effort`) are documented in `reference/frontmatter-cheatsheet.md`.

## Installing and testing an example

```bash
# Install a skill into personal scope (~/.claude/skills/)
bash scripts/install-examples.sh 01-basic/lesson-01-anatomy/examples/hello-skill personal

# Install into project scope (.claude/skills/ in CWD)
bash scripts/install-examples.sh 01-basic/lesson-01-anatomy/examples/hello-skill project

# Test interactively
claude
# then: /hello-skill

# Test headless
claude -p "/hello-skill"
```

## Adding content

- Every example skill must be immediately runnable after `bash scripts/install-examples.sh`. No placeholders, no TODOs.
- Every new lesson directory needs a `README.md`.
- Python scripts in `scripts/` subdirectories of examples should be standard library + minimal dependencies (pypdf is the only approved third-party dependency currently in use).
- The `__pycache__` directories are covered by `.gitignore`; do not commit them.
- Commit messages: English, imperative mood, one logical change per commit.

## Key reference files

- `reference/frontmatter-cheatsheet.md` — all fields, portability column, invocation matrix
- `reference/substitution-variables.md` — `$ARGUMENTS`, `$N`, `$name`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`
- `reference/headless-mode.md` — `claude -p` patterns and CI recipes
- `reference/troubleshooting.md` — skill not found, budget overflow, `/doctor`
- `00-introduction/progressive-disclosure.md` — the 3-stage load model (when to use `references/`)
