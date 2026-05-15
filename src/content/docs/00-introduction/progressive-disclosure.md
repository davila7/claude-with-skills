---
title: "Progressive Disclosure: How Skills Load in Three Stages"
---

One of the most important properties of the AgentSkills model is that it does not load everything at once. Context is a finite resource, and loading every skill in full at startup would be wasteful and slow. Instead, skills follow a three-stage loading model that keeps context usage close to zero until a skill is actually needed.

## Stage 1 — Discovery

When Claude Code starts, it scans the skills directories and loads only the `name` and `description` fields from each `SKILL.md` frontmatter. No body, no supporting files.

Cost: approximately 100 tokens per skill.

This is enough for the agent to know what skills exist and what they do. When you type a request, Claude compares the request against the descriptions it has already loaded and decides which skill, if any, to activate.

With 50 skills installed, Stage 1 costs around 5,000 tokens — less than a single medium-length conversation message.

## Stage 2 — Activation

When the agent decides a skill matches the current task (either because you invoked it by name with `/skill-name`, or because the description matched your request), it loads the full body of `SKILL.md`.

Recommended body size: under 5,000 tokens / 500 lines.

This is where your procedure lives: the steps, the decision rules, the output format, the edge cases. Once the body is loaded, the agent follows those instructions to complete the task. At this point, only the one skill you need is in context — the other 49 are still at Stage 1.

## Stage 3 — Execution

Supporting files — anything in `references/`, `scripts/`, `assets/`, or other subdirectories — are not loaded as part of Stage 2. They load only when the agent explicitly reads or runs them during task execution.

This means you can have a skill whose body is 200 lines with five reference documents totaling 2,000 lines, and none of the reference content loads until the agent reaches the step that says "read references/api-conventions.md".

## What this means in practice

You can install as many skills as you need without worrying about context bloat. The cost model is:

- 50 skills installed, none activated: ~5,000 tokens (Stage 1 for all)
- 50 skills installed, one activated, no references read: ~5,000 + body tokens
- 50 skills installed, one activated, two reference files read: ~5,000 + body tokens + reference file tokens

The design encourages you to write focused skill bodies and push detail into reference files.

## Practical tip: when to move content to references/

If your skill body grows beyond roughly 80 lines, read through it and ask which parts are always needed and which parts are only needed for specific cases. Move the case-specific detail into `references/` files. From the skill body, link to them explicitly:

```markdown
For the full list of supported API error codes, see references/error-codes.md.
```

Claude will read that file when it reaches that instruction. Until then, it stays out of context. This keeps Stage 2 fast and leaves more room for the actual task content.
