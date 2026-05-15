---
title: "Lesson 05: Skills Orchestrating Skills"
---

Skills cannot directly call each other. However, a skill's body can instruct Claude to invoke other skills by name. When Claude reads "run `/changelog-entry` first, then `/tag-version`", it executes those slash commands in sequence using the Skill tool.

This lesson covers the orchestration pattern, when to use it, and a realistic release workflow that demonstrates it.

---

## How skills call other skills

An orchestrator skill does not contain any special invocation mechanism. It is plain natural language that tells Claude what to do. Claude, reading the instructions, recognizes `/skill-name` references and invokes them.

**Why this works:**

1. Claude reads the orchestrator skill's body.
2. The body instructs Claude to invoke `/other-skill-name`.
3. Claude uses the Skill tool to invoke that skill.
4. The invoked skill runs completely and returns.
5. Claude reads the next instruction in the orchestrator and proceeds.

Each invocation completes before the next begins. The orchestrator sees the full output of each step before moving on.

**A minimal example:**

```markdown
## Orchestrator body

Run the release workflow:

1. Run `/changelog-entry` to generate the changelog entry.
2. Review the output with the user — confirm it is accurate.
3. Run `/tag-version` to create the git tag.
4. Run `/publish` to push the tag and create the GitHub release.
```

Claude reads this as a sequence of instructions. It invokes each skill in order, waits for results, and proceeds.

---

## When to orchestrate versus consolidate

**Orchestrate when:**

- Each sub-skill is also useful on its own. A developer may want to run `/changelog-entry` without doing a full release, or `/publish` independently after a manual tag.
- Different people use different steps. A release manager may handle tagging; a CI job may handle publishing.
- Human review is needed between steps. An orchestrator can pause at any step and ask for confirmation before proceeding.

**Consolidate into one skill when:**

- The steps are always run together with no variation.
- No one needs the individual pieces.
- You want the simplest possible user experience.

If you can think of a reason to run any step in isolation, keep the skills separate and write an orchestrator.

---

## Ordering guarantees

Each skill invocation completes before the next instruction executes. This means:

- The orchestrator can check the output of step 1 before running step 2.
- If a step fails, Claude can stop and report the failure rather than blindly continuing.
- Conditional logic is possible: "If `/security-scan` returns any critical findings, stop here and ask the user."

---

## Example: release-flow

The `examples/release-flow/` directory contains a complete multi-step release workflow:

| Skill | What it does |
|---|---|
| `/release` | Orchestrator — invokes the other three in sequence |
| `/changelog-entry` | Drafts a Keep a Changelog entry from recent commits |
| `/tag-version` | Bumps the version and creates an annotated git tag |
| `/publish` | Pushes to origin and creates a GitHub release |

**To try it:**

```bash
cp -r examples/release-flow/.claude/skills ~/.claude/skills
```

Open Claude Code in a git repository and run:

```
/release 1.2.0
```

Claude will invoke `/changelog-entry`, show you the result, ask for confirmation, then run `/tag-version 1.2.0` and `/publish` in sequence.

**To use the individual skills without the orchestrator:**

```
/changelog-entry
/tag-version patch
/publish
```

Each works independently. The orchestrator exists to chain them when you want the full workflow in one command.

---

## Writing effective orchestrators

**Be explicit about what Claude should do with each step's output.**

Weak:

```markdown
1. Run `/security-scan`
2. Run `/complexity-check`
3. Run `/publish`
```

Better:

```markdown
1. Run `/security-scan`. If any CRITICAL findings are returned, stop and tell the user. Do not proceed to step 2.
2. Run `/complexity-check`. Note any warnings for the final report.
3. Run `/publish` only after the user confirms they want to proceed.
```

**Pre-flight the environment before invoking sub-skills.**

Use a dynamic context injection at the top of the orchestrator to check prerequisites before spending time invoking sub-skills:

```markdown
Current git state:
!`git status --short`

Current tags:
!`git tag --sort=-version:refname | head -5`

If the working tree is dirty (uncommitted changes in the status above), stop and tell the user to commit or stash before running the release workflow.
```

**Name the orchestrator after the workflow, not after what it does internally.**

- Good: `release`, `deploy`, `code-quality-gate`
- Avoid: `run-all-release-steps`, `invoke-changelog-then-tag`

The user thinks about the outcome, not the mechanism.

---

## Next lesson

[Lesson 06: Context window mastery](../lesson-06-context-window-mastery/)
