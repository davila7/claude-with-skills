# Lesson 07: Hooks in Skills

Skills can define hooks that run during the skill's lifecycle. Hooks are shell commands triggered by tool use events. They run outside Claude's turn — they are not LLM calls — which makes them reliable, fast, and suitable for side effects that must happen on every matching tool use regardless of what Claude is doing.

---

## Available hook events

**`PreToolUse`**
Runs before Claude uses a tool. The hook receives the tool name and input via stdin. It can:
- Exit 0: allow the tool use to proceed
- Exit 1: log an error, but the tool use proceeds
- Exit 2: block the tool use — stderr is returned to Claude as an error message

Use `PreToolUse` for: validation, rate limiting, confirmation of dangerous operations, logging.

**`PostToolUse`**
Runs after Claude has used a tool and received the response. The hook receives the tool name, input, and response via stdin. It cannot block (the tool use already completed), but it can trigger side effects.

Use `PostToolUse` for: formatting code after edits, sending notifications, logging, updating external systems.

**`Stop`**
Runs when the skill's subagent completes. Only meaningful for skills with `context: fork` — it maps to `SubagentStop` at runtime.

Use `Stop` for: cleanup after a forked research skill, sending a summary notification when a long-running skill finishes.

---

## Hook format in skill frontmatter

```yaml
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/format.sh"
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-bash.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/on-complete.sh"
```

Each event accepts a list of matcher entries. Each entry has a `matcher` and a list of `hooks` under it. The `matcher` is a string supporting `|` for OR — it matches against the tool name.

**Examples of matchers:**

| Matcher | Matches |
|---|---|
| `"Edit"` | Edit tool only |
| `"Write"` | Write tool only |
| `"Edit\|Write"` | Either Edit or Write |
| `"Bash"` | Any Bash call |
| `"Read"` | Read tool only |

---

## Hook input format

Hooks receive a JSON object via stdin. The structure depends on the event:

**PreToolUse:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

**PostToolUse:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  },
  "tool_response": {
    "filePath": "/path/to/file.ts"
  }
}
```

The `tool_response` structure varies by tool. For `Edit` and `Write`, it includes `filePath`. For `Bash`, it includes `stdout` and `stderr`.

---

## Exit codes

| Code | Effect |
|---|---|
| 0 | Success — proceed normally |
| 1 | Non-fatal error — logged, but execution continues |
| 2 | Block (PreToolUse only) — stderr sent to Claude as error message |

`PostToolUse` hooks should always exit 0. There is nothing to block after the tool has already run, and a non-zero exit code is misleading.

---

## The `${CLAUDE_SKILL_DIR}` variable

Hook commands have access to `${CLAUDE_SKILL_DIR}`, which is the absolute path to the directory containing the `SKILL.md` file. Use it to reference scripts bundled with the skill:

```yaml
command: "bash ${CLAUDE_SKILL_DIR}/scripts/format.sh"
```

This ensures the script is found regardless of the working directory when the hook runs.

---

## Example: auto-format-on-edit

The `examples/auto-format-on-edit/` directory contains a skill that runs Prettier and ESLint automatically after every file edit. This is a `PostToolUse` hook that fires on every `Edit` or `Write` tool call.

**Key characteristics:**
- `user-invocable: false` — users do not invoke this directly; it runs in the background whenever Claude edits a file
- The hook script exits 0 unconditionally — it must not block
- The hook checks whether formatters are installed before running them; missing tools are silently skipped
- The hook extracts the file path from the PostToolUse JSON input and only formats files with recognized extensions

**To activate the skill:**

```bash
cp -r examples/auto-format-on-edit/.claude/skills/auto-format-on-edit ~/.claude/skills/
```

Once installed, every time Claude edits a `.ts`, `.js`, `.jsx`, `.tsx`, `.css`, `.json`, or `.md` file, the hook automatically runs Prettier (and ESLint for script files) on the edited file.

---

## Important constraint: hooks in plugin skills

Skills distributed as plugins cannot define hooks. This is a security restriction — plugins run with limited trust, and hooks have access to the full shell environment.

If a skill that uses hooks needs to be distributed, document the expected hooks in the plugin's README and instruct users to add those hooks to their `.claude/settings.json` globally. Alternatively, users can copy the skill out of the plugin directory into `.claude/skills/` to get hook support.

---

## Next lesson

[Lesson 08: Plugins and distribution](../lesson-08-plugins-and-distribution/README.md)
