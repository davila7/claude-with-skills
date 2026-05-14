# Lesson 01: Progressive Disclosure in Practice

The skills specification recommends keeping SKILL.md under 500 lines. That is a ceiling, not a target. This lesson is about why 80 lines is a better target for the navigator pattern, and how to structure a skill so that the content users rarely need never loads at all.

## The context loading model

Skills load in three stages:

**Stage 1 — Name and description only.** This is what Claude sees when scanning all available skills to decide relevance. Cost: roughly 100 tokens per skill, regardless of how long the body is.

**Stage 2 — SKILL.md body.** This loads when Claude decides the skill is relevant to the current task. Cost: proportional to SKILL.md length.

**Stage 3 — References and supporting files.** These load only if the skill body explicitly tells Claude to read them. Cost: proportional to the file size, and only paid when that subtask comes up.

A 500-line monolithic SKILL.md pays Stage 2 cost on every invocation. A 60-line navigator SKILL.md with four 120-line reference files pays Stage 2 cost every time, but Stage 3 cost only when that specific subtask is needed. If users invoke a PDF extraction skill mostly for text extraction and rarely for form filling, the forms reference almost never loads.

## The navigator pattern

The navigator SKILL.md does three things:

1. Describes what the skill can do (a short paragraph or bullet list)
2. Points to each reference file with a one-sentence description of when to read it
3. Provides a quick-reference table of the most common commands

The one-sentence description for each reference is the critical piece. Claude needs to decide which reference to read based on what the user asked — without reading any of them first. If the description is vague, Claude loads everything to be safe. If the description is precise, Claude loads exactly one.

**Good reference description:** `see [extraction guide](references/extraction.md) — how to handle multi-column layouts, specific page ranges, and table extraction`

**Poor reference description:** `see [extraction guide](references/extraction.md) — more details`

## Recommended structure

```
my-skill/
├── SKILL.md              <- overview + navigation (target: under 80 lines)
├── references/
│   ├── subtask-a.md      <- loaded when task A comes up
│   ├── subtask-b.md      <- loaded when task B comes up
│   └── subtask-c.md      <- loaded when task C comes up
└── scripts/
    └── helper.py         <- executed by Claude, not read into context
```

Scripts in the `scripts/` directory are executed with `Bash` — their source code does not load into context unless Claude explicitly reads them with the `Read` tool. This is another form of progressive disclosure: the implementation details of a script are free until someone asks how the script works.

## Writing reference files

Because reference files load on demand and carry detailed information, they can and should be thorough. Include:

- Exact commands with copy-pasteable flags
- Edge cases and how to handle them
- Error messages the user might see and what they mean
- What to do when the primary approach fails

A 150-line reference file for a rarely-used subtask is not a problem — it loads infrequently and it gives Claude everything it needs when it does load.

## The pdf-toolkit example

The `examples/pdf-toolkit/` directory demonstrates the navigator pattern for a realistic multi-capability skill. The SKILL.md is 35 lines. Three reference files cover extraction, form filling, and merging in detail. Three Python scripts handle the actual file operations.

Install it and test the pattern:

```bash
cp -r examples/pdf-toolkit ~/.claude/skills/
```

Then try:
- `/pdf-toolkit extract my-file.pdf` — Claude reads the SKILL.md navigator and the extraction reference; merging and forms references never load
- `/pdf-toolkit fill my-form.pdf output.pdf name="Jane Smith"` — Claude reads SKILL.md and the forms reference; the other two stay cold

Watch the context cost in the session — it stays proportional to what you actually asked for.

## Next lesson

[Lesson 02: Supporting scripts with ${CLAUDE_SKILL_DIR}](../lesson-02-supporting-scripts/README.md)
