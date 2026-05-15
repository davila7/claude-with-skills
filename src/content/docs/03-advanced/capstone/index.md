---
title: "Capstone: Code Quality Bot"
---

This capstone builds a multi-skill, subagent-backed system that runs code quality checks on the current PR and posts the findings as a GitHub PR comment. It applies every technique from the Advanced section:

- Skills orchestrating other skills (lesson 05)
- Context-efficient skill design (lesson 06)
- Subagents doing isolated research (intermediate lessons, applied here at scale)
- A purpose-built subagent for output formatting and posting (intermediate lesson 04)

---

## What you are building

A code quality gate made of five components:

| Component | Type | What it does |
|---|---|---|
| `code-quality-gate` | Orchestrator skill | Invokes the three scan skills in sequence, then asks `@quality-reporter` to post the combined findings |
| `security-scan` | Research skill | Searches for hardcoded secrets, injection vectors, XSS, insecure defaults |
| `complexity-check` | Research skill | Finds large files, long functions, deep nesting, magic numbers |
| `test-coverage-check` | Research skill | Checks whether changed source files have corresponding test files |
| `quality-reporter` | Subagent | Formats the combined findings into a GitHub PR comment and posts it |

---

## Architecture

```
User invokes /code-quality-gate
  |
  +-- Claude runs /security-scan
  |     (Explore subagent in forked context, read-only)
  |     returns: SECURITY FINDINGS: ...
  |
  +-- Claude runs /complexity-check
  |     (Explore subagent in forked context, read-only)
  |     returns: COMPLEXITY FINDINGS: ...
  |
  +-- Claude runs /test-coverage-check
  |     (Explore subagent in forked context, read-only)
  |     returns: COVERAGE FINDINGS: ...
  |
  +-- Claude invokes @quality-reporter with all findings
        (haiku model, minimal context, one job)
        posts: gh pr comment
        returns: PR comment URL
```

Each scan skill runs in a forked context so its exploration does not inflate the main conversation. The `quality-reporter` subagent is a narrow specialist — it receives the findings as its prompt and has exactly one tool: `gh pr comment`.

---

## What you will build

Complete the project by creating these five files:

1. `.claude/skills/code-quality-gate/SKILL.md` — orchestrator
2. `.claude/skills/security-scan/SKILL.md`
3. `.claude/skills/complexity-check/SKILL.md`
4. `.claude/skills/test-coverage-check/SKILL.md`
5. `.claude/agents/quality-reporter.md`

Read `spec.md` for the acceptance criteria for each component.

A complete reference implementation is in `solution/`. Attempt to build your own version before reading the solution — the specification in `spec.md` gives you enough detail to build the complete system without looking at the solution.

---

## Prerequisites

- Claude Code installed and working
- A git repository with at least one commit and one open pull request (or a branch you can open a PR from)
- `gh` CLI installed and authenticated (`gh auth status`)

---

## Validation

After installing the skills and agent:

1. Open Claude Code in a repository with an open PR.
2. Run `/code-quality-gate`.
3. Verify that:
   - The three scan skills run and each produces a findings section.
   - `@quality-reporter` is invoked with the combined findings.
   - A PR comment is posted (check the PR on GitHub).
   - The comment URL is printed in the Claude Code session.

If no PR is open, the orchestrator should fall back to printing the report to the terminal.

---

## Extension challenges

After completing the base capstone:

1. **Add a `lint-check` skill** — run ESLint or flake8 on changed files and add the output as a fourth section in the quality report.
2. **Gate on severity** — modify `code-quality-gate` to stop and ask for confirmation before posting if any CRITICAL findings are found.
3. **Package as a plugin** — create a `plugin.json` and convert the five components into a distributable plugin following lesson 08.
4. **Add a `PostToolUse` hook** — add a hook to `code-quality-gate` that logs the run to a file in `~/.claude/quality-gate-runs.log` with the timestamp and PR number.
