# Lesson 06: Context Window Mastery

The context window is finite. Every skill description loaded at startup, every invoked skill body, and every tool result competes for the same space. Advanced skill authors must understand how this budget works and how to write skills that stay efficient at scale — when a project has dozens of skills and heavy tool use.

---

## Stage 1: The discovery budget

When Claude Code starts, it loads a listing of all available skills so Claude can decide which to invoke. This listing includes:

- Every skill's `name` — always included, no exceptions
- Every skill's `description` and `when_to_use` — included up to a budget

**Default budget:** approximately 1% of the model's context window.

When the listing overflows the budget, Claude Code truncates descriptions starting with the least-recently-used skills. Skills you invoke frequently keep their full descriptions; rarely-used ones may be truncated to name-only.

**How to check:** Run `/doctor` in Claude Code. It reports whether the skill listing is overflowing and which skills are affected.

**What overflow means in practice:** Claude can still be told to invoke `/skill-name` directly, but it will not automatically recognize when the skill is relevant because the description that would have triggered recognition is missing or truncated.

---

## Stage 2: The body lifecycle

When a skill is invoked, its full `SKILL.md` body enters context as a single message. That message stays in the context for the rest of the session — the skill body is not re-read if you invoke the skill again. The second invocation re-uses the same message.

**Write skill bodies as standing rules, not one-time scripts.** If a skill body reads "Step 1: do X, Step 2: do Y", that reads fine on first invocation. On second invocation, Claude sees those same instructions and must understand whether they apply to the new request. Instructions framed as standing rules ("Always do X before Y when this skill is active") survive re-invocation better.

**After auto-compaction:**

When the context approaches 95% capacity, Claude Code compacts automatically. The compaction summarizes the conversation and re-attaches skill bodies that were previously invoked, subject to a budget:

- Up to 5,000 tokens per skill
- Up to 25,000 tokens total across all re-attached skills
- Skills are prioritized by recency — more recently invoked skills survive compaction; idle skills may be dropped

If a skill stops influencing Claude after compaction, re-invoke it with `/skill-name`.

---

## Stage 3: Auto-compaction and skill survival

Auto-compaction is not optional — it happens automatically when the context fills. Understanding it lets you design skills that survive it gracefully.

**Skills that survive compaction well:**
- Short bodies (under 80 lines) — they fit within the 5,000-token per-skill budget
- Self-contained bodies — they do not depend on earlier conversation turns to make sense
- Skills invoked recently — recency is the primary survival criterion

**Skills that may be dropped after compaction:**
- Rarely invoked skills with large bodies
- `user-invocable: false` background knowledge skills that were loaded early and not re-invoked
- Skills whose bodies reference external state from earlier in the conversation (the state is gone after compaction)

**Recovery:** If a skill that was previously influencing Claude's behavior stops doing so after a long session, run `/skill-name` again. This re-injects the skill body at the current position in the context, where it will be prioritized by recency.

---

## Design principles for context efficiency

### 1. Keep SKILL.md short

Target under 80 lines per skill. If the full instructions require more detail, move the detail to a `references/` directory — Claude can read those files when needed rather than having them always in context.

```
.claude/skills/my-skill/
  SKILL.md              ← under 80 lines, orchestrates the work
  references/
    edge-cases.md       ← loaded only when Claude encounters edge cases
    examples.md         ← loaded only when Claude needs examples
```

The SKILL.md body can instruct Claude: "For edge cases, read `${CLAUDE_SKILL_DIR}/references/edge-cases.md`."

### 2. Descriptions are always-on cost

Every description loads on every session startup. A 512-character description costs 512 characters of the discovery budget every time. Write descriptions that are precise about the trigger condition, not comprehensive about the implementation.

**Too long:**
```yaml
description: This skill runs npm outdated and npm audit to check the project's npm dependencies for packages that are not at their latest version and for packages that have known security vulnerabilities listed in the npm advisory database. It also checks pip dependencies if a requirements.txt is present. Use this skill when you want to know if your dependencies are up to date or when you are about to do a release and want to make sure there are no critical vulnerabilities.
```

**Better:**
```yaml
description: Audit npm and pip dependencies for outdated versions and known vulnerabilities. Use before releases, after adding packages, or when checking package health.
```

Both convey the trigger. The second uses 178 characters instead of 453.

### 3. Background skills still consume description budget

A skill with `user-invocable: false` is still listed in the discovery budget — its description still loads. Only `disable-model-invocation: true` removes a skill from the listing entirely.

Use `user-invocable: false` for: background conventions that Claude should follow but users should not invoke directly.

Use `disable-model-invocation: true` for: skills with side effects that must never run automatically.

If you want a skill that is purely a configuration file and should not cost any description budget: set `disable-model-invocation: true`. The skill is then invisible to Claude's auto-detection and consumes no discovery budget.

### 4. Many small skills beat one large skill

A single 400-line skill body costs 400 lines on every invocation and 400 characters of discovery budget for one description. Four 100-line skills cost 100 lines on each individual invocation (only the invoked one loads) and 100 characters each — but their four focused descriptions give Claude four precise trigger points.

The monolithic skill loads its full body whenever any part of it is needed. The split skills load only what is relevant to the current request.

### 5. The `skillOverrides` setting

In `.claude/settings.json`, you can override per-skill listing behavior:

```json
{
  "skillOverrides": {
    "my-verbose-skill": "name-only",
    "retired-skill": "off"
  }
}
```

- `"name-only"`: the skill appears in the listing with its name but no description. Claude cannot auto-detect when to use it, but users can still invoke it directly.
- `"off"`: the skill is completely hidden from the listing. It does not exist as far as Claude is concerned unless explicitly invoked by name.
- `"user-invocable-only"`: removes the skill from Claude's auto-detection but keeps it in the user's `/` menu.

---

## Tuning knobs

In `.claude/settings.json`:

```json
{
  "skillListingBudgetFraction": 0.02,
  "maxSkillDescriptionChars": 512
}
```

**`skillListingBudgetFraction`** (default: `0.01`)
The fraction of the model's total context window reserved for skill descriptions at startup. Increase this if `/doctor` consistently reports overflow and you have many important skills. Decrease it if you want to maximize the context available for conversation.

**`maxSkillDescriptionChars`** (default: `1536`)
Per-skill cap on the combined `description` + `when_to_use` character count. Skills that exceed this are truncated in the listing. Lowering this forces concise descriptions across the board.

**`SLASH_COMMAND_TOOL_CHAR_BUDGET`** (environment variable)
Override the total discovery budget in characters. Takes precedence over `skillListingBudgetFraction`. Useful for testing the exact overflow threshold during skill development.

---

## Practical workflow for measuring budget

1. Open Claude Code and run `/doctor`.
2. Check the output for "skill listing budget" status.
3. If overflow is reported: identify which skills have the longest descriptions (`description` + `when_to_use` combined character count).
4. For skills that rarely need auto-detection: add `"name-only"` under `skillOverrides` in settings.
5. For skills with side effects that should never auto-activate: confirm `disable-model-invocation: true` is set.
6. Re-run `/doctor` to confirm the budget is no longer overflowing.

---

## Example: lightweight-orchestrator

The `examples/lightweight-orchestrator/` directory contains a `code-quality-audit` skill that demonstrates keeping the SKILL.md body minimal. The skill uses `context: fork` and `agent: Explore` to delegate thorough investigation to a subagent, keeping the skill body itself under 40 lines while still producing a comprehensive audit.

---

## Next lesson

[Lesson 07: Hooks in skills](../lesson-07-hooks-in-skills/README.md)
