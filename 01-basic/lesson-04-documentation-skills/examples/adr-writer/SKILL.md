---
name: adr-writer
description: Write an Architecture Decision Record (ADR) document for a technical decision. Use when documenting a technical choice, architectural decision, or design decision.
---

## Instructions

If the user has not specified a decision topic, ask for it before proceeding. One clarifying question is sufficient — ask for the decision, the context that led to it, and any alternatives they considered.

Write an ADR using the MADR (Markdown Any Decision Records) template below. Fill in all sections based on what the user has provided. Use direct, factual language throughout.

### Template

```markdown
# [Short title describing the decision and its solution]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context

[Describe the problem, constraint, or situation that made this decision necessary.
Include any relevant technical context, business requirements, or constraints.
This section answers: what forced us to make a decision?]

## Decision

[State the decision clearly and directly.
Start with "We will..." or "We decided to..."
Explain the key reasoning in one to three sentences.]

## Alternatives considered

- **[Alternative 1]**: [Brief description]. Rejected because [reason].
- **[Alternative 2]**: [Brief description]. Rejected because [reason].

## Consequences

**Positive:**
- [What becomes easier, faster, or safer as a result]

**Negative:**
- [What becomes harder, more expensive, or constrained as a result]

**Neutral:**
- [Things that change but are neither clearly good nor bad]
```

### Filing the ADR

After writing the document, check whether either of these directories exists:

- `docs/adr/`
- `docs/decisions/`

If one exists, offer to save the file there with a filename following the pattern `NNNN-short-title.md` where NNNN is the next sequential number (check existing files to determine the sequence). If neither directory exists, output the document to the conversation and suggest the user create `docs/adr/` and save it there.

### One ADR per decision

Do not combine multiple decisions into one ADR. If the user describes two distinct decisions, write two separate ADRs.
