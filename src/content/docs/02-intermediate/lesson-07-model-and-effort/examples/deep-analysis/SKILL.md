---
title: "deep-analysis"
name: deep-analysis
description: Perform a deep architectural analysis or security review requiring extended reasoning. Use for complex architecture decisions, security audits, or when standard analysis is not finding the root cause.
model: opus
effort: high
disable-model-invocation: true
---

## Deep analysis

ultrathink

Perform a thorough analysis of the described problem or codebase area. Do not skip steps under time or context pressure. This skill intentionally uses extended reasoning — use it.

### Step 1: Gather all relevant context

Before forming any hypothesis, collect the raw material:

- Read all files directly involved in the problem area
- Check git history for the relevant files: `git log --oneline --follow -20 <file>` for each key file, then `git show <hash>` for commits that look relevant
- Look for tests that cover the area: they describe the intended behavior
- Look for related configuration (environment variables, feature flags, build configuration)
- Check for any documentation: comments, ADRs, or README sections that mention the area

Do not stop gathering context when you think you understand the issue. The full picture often requires reading more than the most obvious files.

### Step 2: Identify the core issue or question

State, in one or two sentences, what the fundamental question or problem is. Separate it from symptoms. For example:

- Symptom: "The API returns 500 errors intermittently"
- Core question: "Is this a race condition in the connection pool, an unhandled exception in a specific code path, or an infrastructure issue?"

If you are doing an architectural analysis, state the specific decision or tradeoff being evaluated.

### Step 3: Consider multiple hypotheses or approaches

Do not converge on the first plausible explanation. List at least three distinct hypotheses or approaches:

- For bug analysis: three distinct root causes that could explain the observed behavior
- For architecture decisions: three distinct design approaches with different tradeoff profiles
- For security reviews: three distinct vulnerability classes to investigate

For each, note what evidence would confirm or rule it out.

### Step 4: Evaluate tradeoffs

For each hypothesis or approach, evaluate:

**Evidence for**: What in the codebase supports this explanation or approach?
**Evidence against**: What contradicts it or makes it unlikely?
**Risk**: If this hypothesis is wrong or this approach is chosen, what goes wrong?
**Cost to verify or implement**: How much effort would confirming or executing this require?

Work through the evidence systematically. Update your confidence in each hypothesis as you find more evidence. It is correct to change your assessment mid-analysis — note when you do and why.

### Step 5: Give a concrete recommendation with justification

State the conclusion clearly:

- For bug analysis: the most likely root cause, the specific code location (file and line number), and the minimal fix
- For architecture decisions: the recommended approach and the specific reasons it is better than the alternatives for this codebase and team context
- For security reviews: each vulnerability found (severity, affected code path, file:line reference), the remediation, and any areas that need further investigation by a human

Do not hedge to the point of uselessness. If the evidence points to one conclusion, say so. If there is genuine uncertainty, say specifically what information would resolve it.

### Notes

Cite specific files and line numbers for every specific claim. A claim without a file:line reference is an opinion, not a finding.
