---
title: "summarize-changes-headless"
name: summarize-changes-headless
description: Summarizes uncommitted git changes in a concise machine-readable format. Use in CI pipelines, scripts, or headless invocations where the output will be piped or captured.
---

## Current changes

!`git diff HEAD`

## Instructions

If the diff above is empty, output exactly: `No uncommitted changes.`

Otherwise, output the summary in the following format with no surrounding prose:

```
SUMMARY
- [bullet point describing the first logical change]
- [bullet point describing the second logical change]
[continue as needed, two to five bullets maximum]

RISKS
- [risk] or NONE
```

Rules for the SUMMARY section:
- Each bullet describes a logical change, not a file change. If three files were modified to implement one feature, that is one bullet.
- Use present tense: "Add validation for email field" not "Added" or "Adding".
- Maximum 80 characters per bullet.

Rules for the RISKS section:
- List only genuine risks: missing error handling, hardcoded credentials, removed tests, breaking API changes.
- If there are no risks, write NONE on a single line.
- Do not list stylistic observations as risks.

Output nothing else. No preamble, no "Here is the summary:", no closing remarks. The output must be parseable by a script that splits on the SUMMARY and RISKS headers.

---

Note: this skill is optimized for headless use with `claude -p "/summarize-changes-headless"`. The concise, structured output can be captured with `claude -p "/summarize-changes-headless" > summary.txt` and processed by downstream tools. Compare this to the interactive `summarize-changes` skill, which produces more readable prose suited to an interactive session. In headless mode, conciseness and consistent structure matter more than readability, because there is no follow-up turn to ask for clarification or a reformatted response.
