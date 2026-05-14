---
name: pdf-toolkit
description: Extract text and tables from PDFs, fill PDF form fields programmatically, and merge multiple PDF files into one. Use when working with PDF documents, form filling, document extraction, splitting, or any PDF manipulation task.
allowed-tools: Read Bash(python3 *) Bash(pip install *)
---

Process PDF files using the bundled scripts.

## Capabilities

- **Text extraction**: read text content from any PDF page or page range → see [extraction guide](references/extraction.md) for multi-column layouts, page ranges, table extraction, and OCR limitations
- **Form filling**: fill PDF form fields programmatically and flatten the result → see [forms guide](references/forms.md) for listing fields, setting values, checkboxes, radio buttons, and flattening
- **Merging and splitting**: combine multiple PDFs, reorder pages, add bookmarks, or split into individual pages → see [merging guide](references/merging.md) for all merge and split operations

## Quick reference

| Task | Command |
|------|---------|
| Extract all text | `python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py <input.pdf>` |
| Extract page range | `python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py <input.pdf> --pages 2-5` |
| Fill form | `python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py <input.pdf> <output.pdf> field=value ...` |
| Merge PDFs | `python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py <out.pdf> <in1.pdf> <in2.pdf> ...` |

## Instructions

1. Identify which operation the user needs: extraction, form filling, or merging/splitting.
2. Read the relevant reference file for detailed instructions and edge case handling.
3. Run the appropriate script from `${CLAUDE_SKILL_DIR}/scripts/`.
4. If a required library (`pypdf`, `pdfplumber`) is not installed, offer to install it with `pip install <library>` before retrying.
5. Report the output file path or print the extracted text to the user.
