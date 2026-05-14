# Troubleshooting Skills

Diagnostic guide for the most common skill problems.

---

## Skill Not Appearing in the / Menu

**Step 1: Check the directory name and the `name` frontmatter field.**

The spec requires the directory name to match the `name` field. If they diverge, the skill may fail to register. Verify both:

```bash
ls ~/.claude/skills/         # directory names
grep "^name:" ~/.claude/skills/*/SKILL.md   # name fields
```

**Step 2: Verify SKILL.md exists directly in the skill directory.**

The file must be at `skill-name/SKILL.md`, not nested further. `skill-name/src/SKILL.md` is not recognized.

**Step 3: Check the name value.**

Valid names are lowercase, use hyphens as separators, do not contain consecutive hyphens (`--`), do not start or end with a hyphen, and are at most 64 characters. A name like `my--skill` or `-skill` will fail to register.

**Step 4: Check `user-invocable`.**

If `user-invocable: false` is set, the skill is intentionally hidden from the `/` menu. That is correct behavior. If you want it in the menu, remove that field or set it to `true`.

**Step 5: Restart Claude Code.**

Claude Code scans for skills at startup. If you created a new skills directory while Claude Code was already running, the new directory is not detected until restart. Edits to existing SKILL.md files within already-known directories are live-reloaded without a restart. New directories require a restart.

---

## Skill Not Triggering Automatically

**Step 1: Confirm Claude can see the skill.**

Ask Claude directly: "What skills are available?" Claude will list what it can see, which reveals whether the skill is registered and whether its description is intact.

**Step 2: Check the description for trigger keywords.**

Claude matches user requests to skill descriptions using semantic similarity. If the description uses technical jargon but users phrase requests in plain language (or vice versa), Claude may not make the connection. Revise the description to include the natural language phrases users actually type.

**Step 3: Verify `disable-model-invocation` is not set.**

`disable-model-invocation: true` completely hides the skill from Claude. If this field is set, Claude will never auto-invoke it, regardless of what the user says.

**Step 4: Check the description budget with `/doctor`.**

Run `/doctor` in Claude Code. If the description budget is overflowing, some skill descriptions are being dropped. A skill whose description is dropped cannot auto-invoke. See the invocation matrix reference for tuning options.

**Step 5: Try rephrasing your request.**

Match the skill description more literally to test whether the description is the issue. If invoking with phrasing that closely mirrors the description works but natural phrasing does not, the description needs more keyword coverage.

**Step 6: Invoke directly to confirm the skill works.**

Run `/skill-name` manually. If it works correctly when manually invoked, the skill body is fine and only the auto-invocation trigger needs improvement. Strengthen the description and `when_to_use` fields.

---

## Skill Triggering Too Often

**Step 1: Make the description more specific.**

Add qualifiers that narrow the scope. "Only when the user explicitly asks to..." or "Specifically for tasks involving..." reduce false positives.

**Step 2: Add `disable-model-invocation: true`.**

If auto-invocation is not needed at all, disable it. The skill remains available to users via `/name` without Claude triggering it spontaneously.

**Step 3: Use `paths` to restrict to relevant files.**

If the skill is file-type-specific (e.g., a Python formatter), add a `paths` field so it only surfaces when the session involves matching files:

```yaml
paths:
  - "**/*.py"
```

**Step 4: Split into two skills.**

Create one version with `disable-model-invocation: true` for user-controlled invocation and a separate version with a narrow description for auto-invocation on a specific, well-defined trigger. This is cleaner than trying to make a single description precise enough to auto-invoke rarely.

---

## !`cmd` Output Not Appearing

**Step 1: Check `disableSkillShellExecution`.**

If `disableSkillShellExecution: true` is set in settings (project or user), all inline shell execution in skills is disabled. Shell blocks silently produce no output. Remove or set to `false` to re-enable.

**Step 2: Test the command independently.**

Copy the command from the skill body and run it in your terminal. If it fails outside the skill, it will fail inside the skill too. Fix the command first.

**Step 3: Check the working directory.**

Shell commands in skill blocks run in the project directory (the directory Claude Code was opened in), not the skill directory. Commands that assume they are running from the skill directory will fail or produce wrong output. Use `${CLAUDE_SKILL_DIR}` to reference files relative to the skill:

```
!`python3 ${CLAUDE_SKILL_DIR}/scripts/check.py`
```

**Step 4: Check stderr.**

If the command exits non-zero, Claude receives the error output instead of the expected output. This is often more informative than the original expected output — Claude will typically describe the error. Address the underlying command error.

---

## $ARGUMENTS Substitution Not Working

**Step 1: Confirm substitution tokens appear in the body, not only in frontmatter.**

`$ARGUMENTS`, `$0`, `$1`, and `$name` are substituted in the SKILL.md body text only. They have no effect in frontmatter fields. If you want Claude to know the argument value, it must appear somewhere in the body.

**Step 2: Check named argument configuration.**

If using `$name` syntax, verify the `arguments:` frontmatter field exists and lists the argument names in order. The names must match exactly — `$component` requires `component` in the arguments list. A mismatch leaves `$component` as a literal string rather than expanding it.

**Step 3: Quote multi-word arguments.**

Arguments are split on whitespace. `/my-skill hello world` gives `$0 = "hello"` and `$1 = "world"`. If you intend `hello world` as a single argument, invoke with quotes: `/my-skill "hello world"`, which gives `$0 = "hello world"`.

---

## Skill Description Budget Overflow

**Symptom:** Claude stops auto-invoking skills that used to work. Skills appear in `/doctor` as truncated or dropped.

**Step 1: Run `/doctor`.**

This command reports the current description budget usage, which skills have truncated descriptions, and by how much the budget is exceeded.

**Step 2: Set low-priority skills to name-only.**

In `.claude/settings.local.json`, mark skills that Claude rarely needs to auto-invoke:

```json
{
  "skillOverrides": {
    "my-reference-skill": "name-only",
    "my-seldom-used-skill": "name-only"
  }
}
```

Name-only skills still appear in the `/` menu and still work when invoked, but their descriptions are not included in Claude's context, freeing budget for higher-priority skills.

**Step 3: Increase the budget fraction.**

In `.claude/settings.json`:

```json
{
  "skillListingBudgetFraction": 0.02
}
```

The default is `0.01` (1% of context). Doubling to `0.02` gives descriptions twice as much space.

**Step 4: Trim description text.**

Put the key trigger phrase at the start of each description. Cut boilerplate like "This skill is designed to..." or "Use this skill when you want to...". Every character counts toward the per-skill cap of 1536 characters.

---

## Skill Stops Influencing Behavior After First Response

The skill body does not expire from context. It is still there. The model is choosing other behavior. There are three common causes:

**Cause 1: Compaction trimmed the skill body.**

After auto-compaction, skills are re-attached at a 5000-token cap per skill and 25000-token total. If the skill body was longer than 5000 tokens, the truncated version may be missing critical instructions. Re-invoke the skill with `/skill-name` to restore the full content.

**Cause 2: Competing context is outweighing the skill.**

In a long session, many messages and file contents accumulate in context. More recent context carries more influence. If the skill's instructions were loaded early in the session and a lot has happened since, the model may prioritize recent context. Re-invoke the skill to move its content to the current position in context.

**Cause 3: The description or body needs stronger instruction language.**

Add explicit instruction language to the skill body: "Always...", "Every time you...", "Without exception...". Vague guidance like "consider using..." is easy for the model to override when other signals point a different direction.

---

## allowed-tools Not Pre-Approving a Tool

**Step 1: Accept the workspace trust dialog.**

For project-scoped skills (`.claude/skills/`), Claude Code requires you to accept a workspace trust prompt for the project folder before `allowed-tools` takes effect. If you have not accepted trust for this project, tool pre-approval is silently inactive.

**Step 2: Check the syntax.**

`allowed-tools` is a space-separated string with case-sensitive tool names. Common mistakes:

```yaml
# Wrong — lowercase bash
allowed-tools: bash read write

# Correct — title case
allowed-tools: Bash Read Write
```

For tool+pattern combinations:

```yaml
# Wrong — no space around parens
allowed-tools: Bash(git*)

# Correct — space before paren pattern
allowed-tools: Bash(git *)
```

**Step 3: Remember that allowed-tools pre-approves, it does not restrict.**

Tools listed in `allowed-tools` run without a permission prompt. Tools not listed still work but prompt as normal. If you see prompts for tools not in your list, that is expected behavior.

**Complete list of tool names for reference:**

`Read`, `Write`, `Edit`, `MultiEdit`, `Bash`, `Grep`, `Glob`, `LS`, `WebFetch`, `WebSearch`, `Skill`, `Agent`, `TodoRead`, `TodoWrite`

Exact capitalization is required.
