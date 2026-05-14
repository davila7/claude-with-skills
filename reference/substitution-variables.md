# String Substitution Variables

Claude Code replaces substitution tokens in SKILL.md bodies before passing the content to the model. This reference covers every available substitution with practical examples.

---

## $ARGUMENTS

Contains the full argument string exactly as the user typed it after the skill name. No parsing, splitting, or processing — it is the raw remainder of the invocation line.

**Examples:**

`/fix-issue 123`
- `$ARGUMENTS` = `"123"`

`/migrate-component SearchBar React Vue`
- `$ARGUMENTS` = `"SearchBar React Vue"`

`/deploy staging --dry-run`
- `$ARGUMENTS` = `"staging --dry-run"`

**Important:** If the skill body does not contain `$ARGUMENTS` anywhere, Claude Code automatically appends `ARGUMENTS: <value>` at the end of the skill content when the user provides arguments. This means you do not have to use `$ARGUMENTS` explicitly if you just want Claude to see the value — but using it explicitly lets you control placement and phrasing.

---

## $ARGUMENTS[N] and $N

Index-based access into whitespace-split arguments. Shell quoting is respected: quoted strings with spaces count as a single argument.

Zero-based indexing.

**Examples:**

`/migrate-component "my widget" React Vue`
- `$ARGUMENTS[0]` = `"my widget"` (quotes preserved the space)
- `$ARGUMENTS[1]` = `"React"`
- `$ARGUMENTS[2]` = `"Vue"`
- `$0` = `"my widget"` (shorthand for `$ARGUMENTS[0]`)
- `$1` = `"React"`
- `$2` = `"Vue"`

**Out-of-bounds:** An index that exceeds the number of provided arguments expands to an empty string. The skill should handle this gracefully, typically by documenting required arguments in the body.

---

## $name (Named Arguments)

Named arguments require the `arguments` frontmatter field listing argument names in order. Claude Code then maps positional arguments to those names.

**Frontmatter:**

```yaml
arguments:
  - component
  - source_framework
  - target_framework
```

**Invocation:**

`/migrate-component SearchBar React Vue`

**Expansions:**
- `$component` = `"SearchBar"`
- `$source_framework` = `"React"`
- `$target_framework` = `"Vue"`

Named arguments are more readable than index-based access when a skill has more than one or two arguments. The names appear in the skill body exactly as listed in the `arguments` field, prefixed with `$`.

---

## ${CLAUDE_SESSION_ID}

A UUID that identifies the current Claude Code session. It is stable for the entire session and changes each time Claude Code starts a new session (each `claude` invocation or new session window).

**Use cases:**
- Naming log files so each session's output goes to its own file
- Creating temporary directories scoped to a session that can be cleaned up later
- Correlating output files, cached results, or intermediate artifacts across multiple skill invocations in the same session

**Example usage in skill body:**

```
Log all output to /tmp/claude-${CLAUDE_SESSION_ID}/analysis.log for later review.
```

---

## ${CLAUDE_EFFORT}

The current effort level as a string. Possible values: `low`, `medium`, `high`, `xhigh`, `max`.

The value reflects the effort setting active for the session, unless the skill frontmatter overrides it with the `effort` field — in which case `${CLAUDE_EFFORT}` reflects the overridden value.

**Use case:** Adapt skill behavior based on effort. At high effort, produce detailed reasoning and extensive output. At low effort, produce concise summaries.

**Example usage in skill body:**

```
Current effort level: ${CLAUDE_EFFORT}

If effort is low or medium: produce a one-paragraph summary.
If effort is high, xhigh, or max: produce a full structured report with section headers, findings, and recommendations.
```

---

## ${CLAUDE_SKILL_DIR}

The absolute path to the directory containing the SKILL.md file. This is stable regardless of where the skill is installed (personal scope, project scope, or a plugin).

**Example values by scope:**
- Personal: `/Users/you/.claude/skills/my-skill`
- Project: `/Users/you/myproject/.claude/skills/my-skill`
- Plugin: `/Users/you/.claude/plugins/my-plugin/skills/my-skill`

**Critical rule:** Always use `${CLAUDE_SKILL_DIR}` when referencing bundled scripts, templates, config files, or any other resource that ships alongside the SKILL.md. Never hardcode an absolute path — it will break when the skill is installed in a different location or by a different user.

**Example usage in skill body:**

```
Run the analysis script:
Bash: python3 ${CLAUDE_SKILL_DIR}/scripts/analyze.py --input $0
```

---

## Complete Example: session-report Skill

This example skill uses all five substitution types together. It accepts named arguments for the report format and audience, logs to a session-scoped file, adjusts verbosity based on effort, and delegates to a bundled script.

**Directory structure:**

```
session-report/
  SKILL.md
  scripts/
    collect_session_data.py
```

**SKILL.md:**

```markdown
---
name: session-report
description: Generate a session activity report summarizing what was done in this session. Use when the user asks for a session summary, activity log, or session report.
arguments:
  - format
  - audience
argument-hint: <format> <audience>
---

Generate a session activity report.

Format: $format
Audience: $audience
Full arguments string: $ARGUMENTS

Session ID: ${CLAUDE_SESSION_ID}
Effort level: ${CLAUDE_EFFORT}

Steps:

1. Run the data collection script and capture its output:
   Bash: python3 ${CLAUDE_SKILL_DIR}/scripts/collect_session_data.py --session ${CLAUDE_SESSION_ID}

2. Write the raw output to a session log file:
   Bash: mkdir -p /tmp/claude-sessions && python3 ${CLAUDE_SKILL_DIR}/scripts/collect_session_data.py --session ${CLAUDE_SESSION_ID} > /tmp/claude-sessions/${CLAUDE_SESSION_ID}.log

3. Produce the report in the requested $format for the $audience audience.

Verbosity rules based on effort level ${CLAUDE_EFFORT}:
- low: one paragraph, top three findings only
- medium: structured list, five to ten items
- high or above: full report with sections, timeline, and recommendations

Output only the report content. No preamble.
```

**Invocation:**

`/session-report markdown engineering-team`

**What each substitution resolves to:**
- `$format` = `"markdown"`
- `$audience` = `"engineering-team"`
- `$ARGUMENTS` = `"markdown engineering-team"`
- `${CLAUDE_SESSION_ID}` = `"a3f2c1d8-..."` (actual session UUID)
- `${CLAUDE_EFFORT}` = `"medium"` (or whatever the current session effort is)
- `${CLAUDE_SKILL_DIR}` = absolute path to the `session-report/` directory
