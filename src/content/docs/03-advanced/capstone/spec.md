---
title: "Capstone Specification"
---

Acceptance criteria for each component of the Code Quality Bot. Build to these criteria. The solution in `solution/` is the reference implementation.

---

## `code-quality-gate` skill

**Location:** `.claude/skills/code-quality-gate/SKILL.md`

### Required frontmatter

| Field | Required value |
|---|---|
| `name` | `code-quality-gate` |
| `description` | Must mention: running code quality checks, PR, posting a GitHub comment. Must include a trigger phrase so Claude auto-detects it for code review contexts. |
| `disable-model-invocation` | `true` — this skill has side effects (it posts a comment) |
| `allowed-tools` | Must include `Bash(gh pr *)` for the pre-flight check |

### Required behavior

1. **Pre-flight:** Run `gh pr view --json number,title,headRefName` to check whether an open PR exists. If no PR is found, note this and plan to print the report to the terminal instead of posting.

2. **Invoke `/security-scan`** and capture the output.

3. **Invoke `/complexity-check`** and capture the output.

4. **Invoke `/test-coverage-check`** and capture the output.

5. **Invoke `@quality-reporter`** with a message that includes all three findings sections. The message must instruct the reporter to format and post the report.

6. **Confirm** that a comment URL was returned. Print it.

### What to output

- If a PR exists: the PR comment URL.
- If no PR exists: the full formatted report printed to the terminal.
- Always: a summary line indicating how many findings were found across all checks.

### Validation

Run `/code-quality-gate` in a repo with an open PR. Confirm a comment appears on the PR within one session.

---

## `security-scan` skill

**Location:** `.claude/skills/security-scan/SKILL.md`

### Required frontmatter

| Field | Required value |
|---|---|
| `name` | `security-scan` |
| `description` | Must mention: security scan, hardcoded secrets, injection, XSS. Must include auto-invocation trigger keywords. |
| `context` | `fork` |
| `agent` | `Explore` |
| `allowed-tools` | Must include `Grep`, `Glob`, `Read`, `Bash(git diff *)`, `Bash(git log *)` |

### Required behavior

1. **Focus on changed files first.** Inject `git diff --name-only HEAD~1` (or equivalent). Prioritize scanning files in this list.

2. **Scan for each of these patterns:**
   - Hardcoded secrets: `password=`, `api_key=`, `secret=`, `token=` followed by a literal value. Exclude `test/`, `spec/`, `*.example`, `*.sample` files.
   - SQL injection risk: f-strings, template literals, or string concatenation embedding variables directly into SQL keywords (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`).
   - XSS vectors: direct `innerHTML` assignment in `.js` or `.ts` files without sanitization.
   - Unvalidated inputs: request body or params used directly in a database call without explicit validation.
   - Insecure defaults: `DEBUG=True`, `CORS allow *`, `verify=False`.

3. **Output format:** Must be exactly:
   ```
   SECURITY FINDINGS:
   - [CRITICAL|HIGH|MEDIUM|LOW] <file>:<line> — <description>
   ```
   Or, if nothing found: `SECURITY FINDINGS: none`

### Validation

Run `/security-scan` in a project that has no obvious security issues. Confirm output starts with `SECURITY FINDINGS:` and ends with either findings or `none`.

---

## `complexity-check` skill

**Location:** `.claude/skills/complexity-check/SKILL.md`

### Required frontmatter

| Field | Required value |
|---|---|
| `name` | `complexity-check` |
| `description` | Must mention: complexity, functions over 50 lines, files over 300 lines, nesting. |
| `context` | `fork` |
| `agent` | `Explore` |
| `allowed-tools` | Must include `Grep`, `Glob`, `Read`, `Bash(find *)`, `Bash(wc *)` |

### Required behavior

1. **Focus on changed files** using the same `git diff --name-only` injection as the security skill.

2. **Check for:**
   - Files over 300 lines: use `find . -name "*.py" -o -name "*.ts" -o -name "*.js" | xargs wc -l | sort -rn | head -20`. Exclude `node_modules`, `dist`, `.git`.
   - Long functions: estimate function lengths by scanning for function/method definitions and measuring the gap to the next definition. Flag functions estimated to be over 50 lines.
   - Deep nesting: grep for 4+ levels of indentation (16+ spaces or 4+ tabs) inside conditionals or loops.
   - Magic numbers: numeric literals other than 0, 1, -1 used directly in conditions or calculations without a named constant.

3. **Output format:** Must be exactly:
   ```
   COMPLEXITY FINDINGS:
   - <file>:<line> — <description>
   ```
   Or, if nothing found: `COMPLEXITY FINDINGS: none`

### Validation

Run `/complexity-check` in a project. Confirm output starts with `COMPLEXITY FINDINGS:` and that any listed items include `file:line` references.

---

## `test-coverage-check` skill

**Location:** `.claude/skills/test-coverage-check/SKILL.md`

### Required frontmatter

| Field | Required value |
|---|---|
| `name` | `test-coverage-check` |
| `description` | Must mention: test coverage, test files, changed files. |
| `context` | `fork` |
| `agent` | `Explore` |
| `allowed-tools` | Must include `Grep`, `Glob`, `Read`, `Bash(git diff *)`, `Bash(find *)` |

### Required behavior

1. **Get changed source files:** Inject `git diff --name-only HEAD~1` and filter out test files, `.md`, `.json`, `.yaml`.

2. **For each changed source file:**
   - Derive expected test file names using common conventions:
     - `src/utils/parser.ts` → `src/utils/parser.test.ts`
     - `src/utils/parser.ts` → `src/utils/__tests__/parser.ts`
     - `src/utils/parser.ts` → `tests/utils/parser.test.ts`
     - `src/utils/parser.ts` → `tests/utils/parser.spec.ts`
   - Use Glob to check if any of these files exist.
   - If a test file is found, check whether it imports or mentions the source file name.

3. **Output format:** Must be exactly:
   ```
   COVERAGE FINDINGS:
   - <source-file> — no test file found
   - <source-file> — test file exists but may not cover new changes
   ```
   Or, if all files have tests: `COVERAGE FINDINGS: none`

### Validation

Run `/test-coverage-check` in a project with some tested and some untested files. Confirm it correctly identifies which files are missing tests.

---

## `quality-reporter` subagent

**Location:** `.claude/agents/quality-reporter.md`

### Required frontmatter

| Field | Required value |
|---|---|
| `name` | `quality-reporter` |
| `description` | Must mention: format code quality findings, post GitHub PR comment. |
| `tools` | `Bash(gh pr comment *)` and `Bash(gh pr view *)` only — no read tools, no write tools |
| `model` | `haiku` — this is a formatting and posting job, not a reasoning job |

### Required behavior

When invoked with a message containing findings from the three scans:

1. **Format the findings** into a markdown PR comment with:
   - A summary table showing the status of each check (count of findings, or "Clean" if none)
   - A section per check with the full findings list
   - A footer line: `Generated by code-quality-gate`

2. **Post the comment:**
   ```bash
   gh pr comment --body "<formatted comment>"
   ```

3. **Return the comment URL** from the `gh pr comment` output.

### What the comment must look like

The comment must contain at minimum:

- The text `## Code Quality Report`
- A table or list showing the count or status of Security, Complexity, and Test Coverage checks
- The full findings for each check (or "No issues found")
- The footer `Generated by code-quality-gate`

### Validation

After running `/code-quality-gate` on a repo with an open PR, open the PR on GitHub. The comment should appear with the correct format and all three sections populated.

---

## Integration test

Run the complete system end-to-end:

1. Open a repository with at least one commit, one source file, and an open pull request.
2. Run `/code-quality-gate`.
3. Confirm:
   - All three scan skills ran (their `FINDINGS:` sections appear in session output)
   - `@quality-reporter` was invoked
   - A PR comment URL was printed
   - The comment on GitHub has the expected format
4. Run it again on a clean PR. Confirm each section shows "none" or "No issues found" appropriately.
