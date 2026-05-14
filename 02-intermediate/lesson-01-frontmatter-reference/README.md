# Lesson 01: Complete Frontmatter Reference

This lesson documents every frontmatter field available in Claude Code Skills. For each field you will find its type, default, a concrete use case, and a counterpoint — when the field is the wrong choice.

## AgentSkills standard fields vs Claude Code-only fields

Skills follow the [AgentSkills.io open standard](https://agentskills.io). Fields defined by that standard are portable: they work in Cursor, GitHub Copilot, Gemini CLI, and any other compliant tool. Claude Code implements the full standard and adds a superset of fields for finer control.

**AgentSkills standard fields** (portable, work in any compliant tool):
- `name`
- `description`
- `allowed-tools`

**Claude Code-only fields** (silently ignored by other tools, degrade gracefully):
- `when_to_use`
- `argument-hint`
- `arguments`
- `disable-model-invocation`
- `user-invocable`
- `model`
- `effort`
- `context`
- `agent`
- `hooks`
- `paths`
- `shell`

If portability matters — you want your skill to run in tools other than Claude Code — use only the standard fields. If you are writing Claude Code-specific workflows, use the full superset.

---

## Field reference

### `name`

- **Type:** String. Lowercase letters, hyphens, and digits only. Maximum 64 characters.
- **Default:** The directory name containing the `SKILL.md` file.
- **Standard:** AgentSkills
- **Use when:** You want the slash command to differ from the directory name, or you want to be explicit about the canonical name in the file itself.
- **Avoid when:** The directory name already matches what you want — the field is optional.
- **Example:**
  ```yaml
  name: dependency-audit
  ```

---

### `description`

- **Type:** Plain text string. Recommended maximum 1,024 characters.
- **Default:** None. Claude has no context about the skill if omitted.
- **Standard:** AgentSkills
- **Use when:** Always. This is the most important field. Claude scans descriptions to decide whether a skill is relevant without being explicitly invoked. Include what the skill does and the keywords a user would naturally type.
- **Avoid when:** There is no meaningful description — in that case, the skill should not exist.
- **Example:**
  ```yaml
  description: Audit npm dependencies for outdated packages and known vulnerabilities. Use when checking package versions, running dependency health checks, or preparing for a release.
  ```

---

### `when_to_use`

- **Type:** Plain text string. Combined with `description`, capped at 1,536 characters total.
- **Default:** None.
- **Standard:** Claude Code only
- **Use when:** The `description` is already at the recommended 1,024-character limit and you need to add more trigger context — for example, a list of additional keywords or edge cases where the skill should activate.
- **Avoid when:** Your `description` already covers when to invoke the skill. Adding `when_to_use` when it is not needed splits the trigger context across two fields for no reason.
- **Example:**
  ```yaml
  when_to_use: Also use when the user asks about security advisories, CVEs, or wants to know if any packages need upgrading before a production deploy.
  ```

---

### `argument-hint`

- **Type:** String displayed in the autocomplete UI.
- **Default:** None. The slash command appears without a hint.
- **Standard:** Claude Code only
- **Use when:** The skill expects one or more arguments and you want to show the user what to type. The hint appears in the `/` menu alongside the skill name.
- **Avoid when:** The skill takes no arguments, or the description already makes the expected input completely obvious.
- **Example:**
  ```yaml
  argument-hint: [package-name]
  ```

---

### `arguments`

- **Type:** Space-separated string or YAML list of names.
- **Default:** None. Arguments are available as `$ARGUMENTS` or `$ARGUMENTS[N]` without this field.
- **Standard:** Claude Code only
- **Use when:** The skill takes multiple positional arguments and you want to reference them by name in the body rather than by index. Named arguments make the body easier to read and maintain.
- **Avoid when:** The skill takes a single free-form argument — use `$ARGUMENTS` directly and skip the overhead of declaring a name.
- **Example:**
  ```yaml
  arguments: [component-name, from-framework, to-framework]
  ```
  In the body, refer to `$component-name`, `$from-framework`, `$to-framework`.

---

### `disable-model-invocation`

- **Type:** Boolean.
- **Default:** `false`. Claude can invoke the skill automatically.
- **Standard:** Claude Code only
- **Use when:** The skill has side effects — it deploys, sends messages, deletes files, pushes to remote, or modifies external state. You do not want Claude to trigger it automatically in response to a user message.
- **Avoid when:** The skill is informational or analytical. Auto-invocation for read-only skills is a feature, not a risk.
- **Example:**
  ```yaml
  disable-model-invocation: true
  ```

---

### `user-invocable`

- **Type:** Boolean.
- **Default:** `true`. The skill appears in the `/` menu and users can invoke it by name.
- **Standard:** Claude Code only
- **Use when:** `false` — when the skill is background knowledge that should inform Claude's behavior rather than an action the user runs. Examples: team API conventions, codebase architecture context, legacy system notes.
- **Avoid when:** The skill is something users should be able to call directly. Hiding a user-facing skill in the `/` menu is confusing.
- **Example:**
  ```yaml
  user-invocable: false
  ```

---

### `allowed-tools`

- **Type:** Space-separated list of tool names. `Bash` accepts an optional glob pattern in parentheses: `Bash(git *)`.
- **Default:** None. Claude prompts for permission before each tool use.
- **Standard:** AgentSkills (the field name is shared; scoped `Bash(pattern)` syntax is Claude Code-specific behavior)
- **Use when:** The skill needs specific tools and you want Claude to use them without prompting. This is especially important for `disable-model-invocation: true` skills, where a permission prompt mid-workflow is disruptive.
- **Avoid when:** You genuinely do not know which tools the skill will need. Guessing and over-permitting is worse than letting the default prompting handle it.
- **Example:**
  ```yaml
  allowed-tools: Read Grep Glob Bash(npm outdated) Bash(npm audit)
  ```

---

### `model`

- **Type:** `haiku`, `sonnet`, `opus`, a full model ID string, or `inherit`.
- **Default:** `inherit` — uses whatever model the current session is running.
- **Standard:** Claude Code only
- **Use when:** The task has a clearly different cost/capability requirement than the session default. Use `haiku` for fast formatting or metadata extraction. Use `opus` for architectural analysis, security reviews, or when the standard model repeatedly misses something.
- **Avoid when:** The skill does a variety of things and no single model is always right. Overriding at the skill level locks every invocation to that model.
- **Example:**
  ```yaml
  model: opus
  ```

---

### `effort`

- **Type:** `low`, `medium`, `high`, `xhigh`, or `max`.
- **Default:** Inherits session effort.
- **Standard:** Claude Code only
- **Use when:** The skill demands deeper reasoning than the session default — a security audit, root cause analysis, or complex refactoring. Or lighter reasoning than the default — simple code generation, file renaming, metadata extraction.
- **Avoid when:** The session default is already appropriate for what the skill does.
- **Example:**
  ```yaml
  effort: high
  ```

---

### `context`

- **Type:** `fork`.
- **Default:** None. The skill runs in the current context.
- **Standard:** Claude Code only
- **Use when:** The skill does large-scale research that would pollute the main conversation context — exploring many files, reading long documents, running many shell commands. Forking prevents skill output from crowding out the user's working context.
- **Avoid when:** The skill needs access to the current conversation history, or the result needs to flow naturally back into an ongoing task.
- **Example:**
  ```yaml
  context: fork
  ```

---

### `agent`

- **Type:** String naming a subagent (e.g., `Explore`).
- **Default:** None. Used in combination with `context: fork`.
- **Standard:** Claude Code only
- **Use when:** `context: fork` is set and you want a specific subagent type to run the skill.
- **Avoid when:** `context: fork` is not set — the `agent` field has no effect without it.
- **Example:**
  ```yaml
  context: fork
  agent: Explore
  ```

---

### `hooks`

- **Type:** YAML map of lifecycle events to shell commands.
- **Default:** None.
- **Standard:** Claude Code only
- **Use when:** You need to run setup or teardown around skill execution — for example, starting a local server before a test skill runs, or posting a Slack notification after a deploy skill completes.
- **Avoid when:** The setup can be done inside the skill body itself. Hooks add complexity; use them only when you need side effects that run outside Claude's turn.
- **Example:**
  ```yaml
  hooks:
    after: echo "Skill completed at $(date)" >> ~/.claude/skill-log.txt
  ```

---

### `paths`

- **Type:** List of glob patterns.
- **Default:** None. The skill is available in all contexts.
- **Standard:** Claude Code only
- **Use when:** The skill should auto-activate only when the user is working with specific file types or directories. A frontend linting skill should not activate when editing a Python migration. Path restrictions make auto-invocation precise.
- **Avoid when:** The skill is general purpose. Restricting paths prevents it from activating in legitimate contexts.
- **Example:**
  ```yaml
  paths:
    - "src/components/**"
    - "src/pages/**"
  ```

---

### `shell`

- **Type:** `bash` or `powershell`.
- **Default:** `bash`.
- **Standard:** Claude Code only
- **Use when:** `powershell` — on Windows environments where dynamic context injection (`` !`cmd` `` blocks) uses PowerShell syntax. Requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` in the environment.
- **Avoid when:** You are on macOS or Linux, or your injection commands are plain POSIX shell. The default `bash` is correct in those cases.
- **Example:**
  ```yaml
  shell: powershell
  ```

---

## String substitutions reference

These substitutions are available in the skill body:

| Substitution | Value |
|---|---|
| `$ARGUMENTS` | The full argument string as typed by the user |
| `$ARGUMENTS[N]` or `$N` | 0-based positional argument (shell-style quoting applies) |
| `$name` | Named argument declared in the `arguments` field |
| `${CLAUDE_SESSION_ID}` | The current Claude Code session identifier |
| `${CLAUDE_EFFORT}` | The current effort level |
| `${CLAUDE_SKILL_DIR}` | Absolute path to the directory containing this `SKILL.md` |

---

## Examples

The `examples/` directory contains one skill that demonstrates how to combine the most commonly paired fields into a practical tool.

- `examples/well-documented-skill/` — a dependency audit skill using `name`, `description`, `when_to_use`, `argument-hint`, and `allowed-tools`

See the README in that directory for a field-by-field explanation of the choices.

## Next lesson

[Lesson 02: Invocation control](../lesson-02-invocation-control/README.md)
