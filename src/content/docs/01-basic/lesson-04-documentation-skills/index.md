---
title: "Lesson 04: Documentation Skills"
---

Documentation is the most common use case for skills. Almost every team has documentation they write repeatedly: READMEs for new projects, ADRs for technical decisions, JSDoc for exported functions, release notes, onboarding guides.

## What makes documentation different from repetitive tasks

Repetitive task skills are mostly about **procedure** — do these steps in this order. Documentation skills are about **knowledge plus format**.

A good documentation skill encodes two things:

1. **What information to gather** — which files to read, which questions to answer, what context matters
2. **How to structure the output** — section order, heading levels, required content, optional sections

Without an opinionated output format, results drift. One developer's README has Installation first, another's puts it after a lengthy introduction. A skill with an explicit template eliminates that inconsistency.

## Consistency as the primary value

When the whole team uses the same `adr-writer` skill, every ADR in the repository follows the same template. A reader opening any ADR knows exactly where to find the context, the decision, and the consequences. They do not need to mentally parse a different layout each time.

This consistency is what separates a documentation skill from just asking Claude to "write a README". The skill is the team's agreement about what a README looks like, captured once and reused forever.

## When to write a documentation skill

- The same documentation type is produced more than once (every project gets a README, every significant decision gets an ADR)
- Different people produce the same document type and the results are inconsistent
- A document type has required sections that are often forgotten (security considerations, license, migration notes)
- The document requires gathering context from the codebase before writing (the agent needs to read files, not just fill in a template)

## Examples in this lesson

| Skill | What it produces |
|-------|-----------------|
| `readme-generator` | A complete README by analyzing the codebase |
| `jsdoc-writer` | JSDoc comments for undocumented functions |
| `adr-writer` | An Architecture Decision Record in MADR format |

## Next lesson

[Lesson 05: Invoking skills](../lesson-05-invoking/)
