---
title: "Budget Tuning Guide"
---

A practical reference for measuring and tuning skill listing budget usage. Apply this when `/doctor` reports overflow, when you have accumulated more than ten skills in a project, or before a planned expansion of your skill set.

---

## Step 1: Check current budget status

Run `/doctor` in Claude Code. Look for the skill listing section in the output. It reports:

- Total characters used by skill descriptions
- Budget limit in characters
- Whether the budget is overflowing
- Which skills are truncated (if any)

If no overflow is reported, your current skill set fits within the budget. You can stop here unless you are planning to add more skills.

---

## Step 2: Identify description-heavy skills

For each skill, count the combined character length of the `description` and `when_to_use` fields. The total of both fields is what counts against the per-skill cap (`maxSkillDescriptionChars`, default 1,536) and the overall discovery budget.

A quick way to count across all skills in a project:

```bash
for f in .claude/skills/*/SKILL.md; do
  skill=$(basename $(dirname $f))
  chars=$(grep -A 200 "^---" "$f" | grep -E "^(description|when_to_use):" | wc -c)
  echo "$chars $skill"
done | sort -rn
```

Skills at the top of the sorted output are consuming the most discovery budget. These are the first candidates for trimming.

---

## Step 3: The `skillOverrides` setting

`skillOverrides` in `.claude/settings.json` lets you control how each skill appears in the listing without modifying the skill files themselves. This is useful when you do not own the skill files (for example, they come from a shared plugin or a team repository).

```json
{
  "skillOverrides": {
    "my-rarely-used-skill": "name-only",
    "legacy-deploy": "off",
    "team-conventions": "user-invocable-only"
  }
}
```

**`"name-only"`**
The skill appears in the listing with its name but without its description. Claude knows the skill exists and users can invoke `/my-rarely-used-skill`, but Claude will not auto-detect when to use it. Use for: skills users know about and invoke manually, but which do not need to appear in Claude's auto-activation logic.

**`"off"`**
The skill is completely hidden from the listing. It does not appear in `/doctor` skill counts, and Claude cannot reference it unless explicitly typed. Use for: skills that are temporarily disabled, skills being tested before release, or skills that exist only for headless mode pipelines.

**`"user-invocable-only"`**
The skill appears in the user's `/` menu (Claude Code's autocomplete) but its description is excluded from Claude's auto-detection listing. This is the right setting for skills you want to be discoverable by users but that should never activate automatically. Use for: skills with side effects that have `disable-model-invocation: true` already, but where you want extra assurance they will not appear in Claude's reasoning.

Settings file precedence (highest to lowest):

1. Project `.claude/settings.local.json` (not committed, developer-specific)
2. Project `.claude/settings.json` (committed, team-shared)
3. User `~/.claude/settings.json` (global, all projects)

`skillOverrides` set in a higher-precedence file wins over lower-precedence files for the same skill name.

---

## Step 4: `disable-model-invocation: true` as a budget tool

Setting `disable-model-invocation: true` in a skill's frontmatter removes that skill's description from the discovery listing entirely. Claude never sees the description at startup and cannot auto-activate the skill.

This is primarily a safety setting for skills with side effects. As a secondary effect, it frees up exactly `len(description) + len(when_to_use)` characters from the discovery budget.

Use it as a budget tool when:

- A skill has a long, detailed description but always needs explicit invocation (the description exists for documentation, not auto-detection)
- A skill is part of an orchestration pipeline and the user never invokes it directly

Do not use it as a budget tool when Claude's auto-detection of the skill is valuable. The savings come at the cost of the skill never activating unless explicitly called.

---

## Step 5: After compaction — which skills survive

When auto-compaction runs, skill bodies that were previously invoked are eligible for re-attachment. The selection criteria:

- **Recency wins**: skills invoked later in the session are more likely to survive
- **Size cap**: each re-attached skill body is capped at 5,000 tokens
- **Total cap**: all re-attached skills together are capped at 25,000 tokens across the session

To check which skills are active after a long session: look at Claude's behavior. If a skill that was influencing Claude's output stops doing so, it has likely been dropped. To confirm, ask: "Which skills are currently active in this session?"

To recover a dropped skill:

```
/skill-name
```

Re-invoking the skill injects its body at the current position in the context. It becomes the most-recent invocation and will survive the next compaction cycle.

---

## Step 6: Settings file locations and hierarchy

**User-level (global across all projects):**
```
~/.claude/settings.json
```

**Project-level (committed, shared with team):**
```
<project-root>/.claude/settings.json
```

**Project-level (local, not committed):**
```
<project-root>/.claude/settings.local.json
```

To set a custom listing budget fraction for a project:

```json
// .claude/settings.json
{
  "skillListingBudgetFraction": 0.02
}
```

This doubles the default discovery budget. Add this when:

- `/doctor` reports overflow and you cannot trim descriptions further
- The project has more than 20 skills that all need active auto-detection
- You are using a model with a very large context window and 1% is an unnecessarily tight cap

To set a stricter per-skill character cap to force concise descriptions across the board:

```json
{
  "maxSkillDescriptionChars": 384
}
```

This prevents any single skill from consuming more than 384 characters of description budget. It is a blunt instrument — prefer trimming individual descriptions first.

---

## Reference: budget math

For a model with a 200,000-token context window (approximately 800,000 characters):

| Setting | Value | Characters for skill listings |
|---|---|---|
| Default `skillListingBudgetFraction` | 0.01 | ~8,000 characters |
| Doubled to 0.02 | 0.02 | ~16,000 characters |
| At default `maxSkillDescriptionChars` 1536 | — | ~5 skills at max description length fit in default budget |
| At trimmed descriptions (200 chars avg) | — | ~40 skills fit in default budget |

The practical takeaway: with tight descriptions averaging 200 characters, the default budget handles approximately 40 skills comfortably. Beyond that, either increase `skillListingBudgetFraction` or use `skillOverrides` to reduce listing weight for less-important skills.
