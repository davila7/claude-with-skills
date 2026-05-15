---
title: "Invocation Matrix and Context Loading"
---

How skill invocation mode, context loading, and the description budget interact.

---

## Part 1: The Invocation Matrix

Two frontmatter fields control who can invoke a skill and what Claude can see:

- `disable-model-invocation: true` — hides the skill from Claude entirely
- `user-invocable: false` — hides the skill from the `/` menu

### Default (neither field set)

Both the user and Claude can invoke the skill. The description appears in Claude's context at session start. The full body loads when either party invokes it.

**Use for:** General-purpose skills, knowledge augmentation, formatting standards, language guides. Most skills belong here.

**Example:** A `/summarize-pr` skill that a developer can invoke manually or that Claude can trigger when it detects the conversation is about reviewing a pull request.

### `disable-model-invocation: true` only

Only the user can invoke the skill via `/name`. Claude never sees the description and cannot auto-invoke it.

**Use for:** Workflows with side effects where you must control timing. Deployments, email sends, database writes, deletions. If Claude could auto-trigger these, a casual mention of "deploy" in conversation could kick off a production deployment.

**Example:** A `/deploy-production` skill. The user decides exactly when to run it. Claude does not know it exists and cannot invoke it accidentally.

### `user-invocable: false` only

Claude can auto-invoke the skill, but it does not appear in the `/` menu for users.

**Use for:** Background expertise that enriches Claude's behavior without cluttering the user-facing skill list. Style guides, coding standards, domain-specific knowledge that Claude should always apply when relevant.

**Example:** A skill encoding your team's code review standards. Claude applies them automatically when reviewing code, but developers never need to invoke `/code-review-standards` manually.

### Both `disable-model-invocation: true` AND `user-invocable: false`

Do not do this. The skill becomes permanently inaccessible — Claude cannot see it and users cannot invoke it. There is no error or warning; the skill simply does nothing. If you want to temporarily disable a skill, rename the SKILL.md file or remove the directory instead.

---

## Part 2: What Loads When

Skill content enters Claude's context in stages. Understanding this prevents surprises about what Claude knows and when.

### At session start

Claude Code scans all skill directories and loads each skill's `name` and `description` (plus `when_to_use` if set) into a tool definition. This costs roughly 100 tokens per skill across a typical skill set.

Claude knows that skills exist and can match user requests to descriptions, but it has not read any SKILL.md bodies yet.

### When a skill is invoked

The full SKILL.md body is injected into the conversation as a single message, at the point of invocation. From that moment forward, all instructions in the body are active for the rest of the session.

Write skill bodies as standing rules, not one-time setup instructions. "Always use 2-space indentation" works correctly. "Set up your indentation preferences now" implies a one-time action after which the instruction is no longer needed — that framing can confuse the model.

### Supporting files

Additional files in the skill directory (scripts, templates, config files) are not loaded automatically. They are only read when Claude explicitly reads them during skill execution (via a `Read` tool call or a `!`cmd`` block that outputs their content). Reference them using `${CLAUDE_SKILL_DIR}` paths in the skill body.

### After context compaction

Claude Code automatically compacts the conversation when context approaches the model's limit. During compaction, the most recent invocation of each skill is re-attached to the compacted context. The budget for re-attached skill content is 5000 tokens per skill and 25000 tokens total across all skills.

Practical implications:
- Long skill bodies (beyond 5000 tokens) will be truncated after compaction.
- If many skills are active, some may be trimmed to fit within the 25000-token aggregate budget.
- If Claude stops following a skill's instructions after a long session, the most likely cause is compaction trimming the skill body. Re-invoking the skill restores the full content.

---

## Part 3: The Description Budget

All skill descriptions must fit within a shared budget. When the budget overflows, Claude loses visibility into some skills and cannot auto-invoke them.

### Budget size

The default budget is 1% of the active model's context window. For a 200,000-token context, that is 2000 tokens for all skill descriptions combined.

### Overflow behavior

When descriptions exceed the budget:
- Descriptions for the least-recently-invoked skills are dropped first.
- Names are always retained even when descriptions drop.
- A skill whose description has been dropped will not auto-invoke, but a user can still invoke it with `/name`.

### Per-skill character cap

The combined text of `description` and `when_to_use` for a single skill is capped at 1536 characters. Content beyond that cap is truncated in the tool definition Claude sees.

Write the most important trigger phrase first in both fields. If the description is truncated, the beginning survives.

### Tuning the budget

Increase the global budget fraction in `.claude/settings.json`:

```json
{
  "skillListingBudgetFraction": 0.02
}
```

Increase the per-skill character cap:

```json
{
  "maxSkillDescriptionChars": 2048
}
```

Set a specific skill to name-only mode in `.claude/settings.local.json`:

```json
{
  "skillOverrides": {
    "my-low-priority-skill": "name-only"
  }
}
```

Override the total budget in characters using the environment variable:

```bash
SLASH_COMMAND_TOOL_CHAR_BUDGET=4000 claude
```

### Checking the budget

Run `/doctor` inside Claude Code. It reports:
- Total description budget in tokens
- Current usage
- Whether any skill descriptions are being truncated
- Which skills are affected

---

## Part 4: Skill Content Lifecycle

### Persistence within a session

Once a SKILL.md body loads into context, it stays there for the rest of the session. There is no expiry. Skills do not re-load on each invocation — the first invocation is the only time the body is injected.

This means re-invoking a skill mid-session does not add a second copy to context. It is a no-op for content loading, but it can signal to Claude to re-apply the skill's instructions.

### Why a skill may stop influencing behavior

A skill that was working can appear to stop working for several reasons:

1. **Description strength:** Claude's auto-invocation depends on the description matching the user's phrasing. If the request is phrased very differently from the description keywords, Claude may not connect the two. Strengthen the description or re-invoke manually.

2. **Competing context:** In a long session with many files, messages, and other instructions in context, the skill's instructions may be outweighed by more recent or more prominent context. Re-invoke the skill to move its content closer to the current point in context.

3. **Compaction:** After auto-compaction, the skill body is re-attached at 5000-token cap. If the original body was longer than 5000 tokens, the truncated version may be missing critical instructions. Re-invoke the skill to reload the full body.

4. **Model choice:** Some models are more instruction-following than others. If you switch to a smaller model mid-session, compliance with detailed skill instructions may decrease.

### Recommended practice

Treat the skill body as a persistent system prompt for that skill's domain. Write rules that should apply throughout the session without needing to be re-stated. Re-invoke skills when you start a new task area or after a long gap in a session.
