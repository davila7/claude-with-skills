---
title: "parallel-investigator"
name: parallel-investigator
description: Investigate two separate areas of the codebase simultaneously and combine findings into a comparison report. Use when you need research on two independent topics at once, want to compare two subsystems, or need to understand how two components relate to each other.
disable-model-invocation: true
argument-hint: "[topic-1] [topic-2]"
---

Investigate these two topics in parallel using separate Explore subagents:

- Topic 1: $0
- Topic 2: $1

## Instructions

1. Spawn two Explore subagents simultaneously — one per topic. Give each a self-contained research prompt that includes:
   - The specific topic to investigate
   - Instructions to search broadly (Grep, Glob) before reading files deeply
   - Instructions to produce a structured report: key files, how it works, notable patterns

   Do not run the subagents sequentially. Start both at the same time.

2. Wait for both subagents to return their results.

3. Combine the findings into a single comparison report with these sections:

   **Topic 1 findings** — summary of what the first subagent found

   **Topic 2 findings** — summary of what the second subagent found

   **Similarities** — patterns, libraries, approaches, or design decisions shared between the two topics

   **Differences** — how they diverge: in scale, in architecture, in data model, in error handling, or in how they are tested

   **Recommendation** — if the user is trying to make a decision (e.g., which approach to follow, which subsystem to extend), give a direct recommendation with reasoning. If the topics are purely informational (e.g., understanding two independent systems), omit this section.

## Note on architecture

This skill does not use `context: fork` — it runs inline in your main conversation. This is intentional: a forked skill cannot spawn additional subagents, so any skill that needs to orchestrate multiple workers must run in the main context and delegate the worker tasks from there. The main conversation is the orchestrator; the Explore subagents are the workers.
