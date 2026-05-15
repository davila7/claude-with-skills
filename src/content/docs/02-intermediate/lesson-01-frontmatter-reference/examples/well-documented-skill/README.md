---
title: "Example: well-documented-skill (dependency-audit)"
---

This skill demonstrates the most commonly combined frontmatter fields for a read-only, user-invocable skill. It audits npm or pip dependencies for outdated packages and vulnerabilities.

## Field choices and rationale

### `name: dependency-audit`

Explicit name declared even though it matches the directory name. This makes the slash command immediately obvious when reading the file without needing to check the directory name.

### `description`

Written for the model, not for humans. It states what the skill does ("audit npm or pip dependencies") and includes keywords a user would naturally type: "checking package health", "preparing for a release", "outdated packages", "security advisories". Claude uses these keywords to decide whether to auto-invoke the skill.

### `when_to_use`

The description covers the main triggers. `when_to_use` adds secondary keywords — "CVEs", "pip check", "dependency rot", "upgrade" — that would not fit naturally in the description without making it verbose. The combined text stays well under the 1,536-character cap.

### `argument-hint: [package-name or "all"]`

The skill works with or without an argument. The hint tells the user exactly what is expected: either a specific package name or the literal string "all" for a full audit. Without this hint, users would not know the skill accepts an argument at all.

### `allowed-tools`

Pre-approves only the commands this skill actually needs:
- `Bash(npm outdated)`, `Bash(npm audit)`, `Bash(npm list *)` — npm inspection commands
- `Bash(pip list *)`, `Bash(pip-audit)`, `Bash(pip show *)` — pip inspection commands
- `Read` — for detecting which package manager files exist

No write tools. No `git` commands. The tool list makes explicit that this skill is read-only. If Claude needed to call `npm install` or `pip install --upgrade`, it would prompt — which is the correct behavior for a skill that is supposed to audit, not modify.

### Fields intentionally omitted

- `disable-model-invocation`: Not set. This skill has no side effects; auto-invocation when the user asks about dependency health is desirable.
- `user-invocable`: Not set (defaults to `true`). Users should be able to call `/dependency-audit` directly.
- `model` / `effort`: Not set. The session default is appropriate for this kind of structured output task.
- `context`: Not set. The audit result should flow naturally back into the conversation.
- `paths`: Not set. The skill should be available regardless of which file the user is currently editing.

## Installing this example

```bash
cp -r examples/well-documented-skill ~/.claude/skills/dependency-audit
```

Then invoke it in any project that has a `package.json` or `requirements.txt`:

```
/dependency-audit
/dependency-audit lodash
/dependency-audit all
```
