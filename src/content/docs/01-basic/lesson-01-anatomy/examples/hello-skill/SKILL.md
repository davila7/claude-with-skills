---
title: "hello-skill"
name: hello-skill
description: Explains what a skill is and demonstrates that skills are working. Use when testing skills, when asked about skills, or when asked to demonstrate how skills work.
---

## Instructions

Greet the user and tell them they just successfully invoked a skill.

Explain what happened in concrete terms:

1. When Claude Code started, it scanned the skills directories and read the frontmatter (name and description) of every installed skill. The body of this file was not loaded yet — only the description was read.

2. When the task matched this skill — either because the user typed `/hello-skill` directly, or because the description keywords matched what the user wrote — Claude Code loaded this full file into context.

3. Right now, Claude is following the instructions written in this body. That is all a skill is: a file of instructions that loads on demand.

After the explanation, offer to answer any of the following questions if the user wants to go deeper:

- How do skills differ from CLAUDE.md?
- How does Claude decide which skill to activate?
- Where do skill files need to be stored?
- How do you write a skill for a repetitive task?

Keep the tone practical and direct. Do not over-explain.
