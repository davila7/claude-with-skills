# PDF Merging and Splitting Reference

This reference covers merging and splitting operations. Read it when the user asks to combine PDFs, merge files, reorder pages, split a PDF into parts, or extract specific pages as a new PDF.

## Basic merge

Combine multiple PDFs into one, in the order provided:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py \
    combined.pdf \
    chapter1.pdf \
    chapter2.pdf \
    chapter3.pdf
```

The output file is the first argument. Input files follow in the desired order. The script handles any number of input files.

## Page ranges within a merge

To include only specific pages from an input file, append a colon and a range:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py \
    report.pdf \
    cover.pdf \
    "body.pdf:2-15" \
    appendix.pdf
```

Range formats:

| Format | Meaning |
|--------|---------|
| `file.pdf:3` | Page 3 only |
| `file.pdf:2-8` | Pages 2 through 8 inclusive |
| `file.pdf:1,4,7` | Pages 1, 4, and 7 |
| `file.pdf:5-` | Page 5 through the last page |

Pages are 1-indexed.

## Reordering pages within a single PDF

To reorder pages in an existing PDF, treat it as a merge with page range selections:

```bash
# Reverse all pages of a 10-page PDF
python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py \
    reversed.pdf \
    "original.pdf:10" \
    "original.pdf:9" \
    "original.pdf:8" \
    "original.pdf:7" \
    "original.pdf:6" \
    "original.pdf:5" \
    "original.pdf:4" \
    "original.pdf:3" \
    "original.pdf:2" \
    "original.pdf:1"
```

For large reordering operations, use pypdf directly:

```python
import pypdf

reader = pypdf.PdfReader("original.pdf")
writer = pypdf.PdfWriter()

# Example: move the last page to the front
order = [len(reader.pages) - 1] + list(range(len(reader.pages) - 1))
for i in order:
    writer.add_page(reader.pages[i])

with open("reordered.pdf", "wb") as f:
    writer.write(f)
```

## Adding bookmarks (outlines)

Bookmarks help readers navigate a merged document. After merging, add top-level bookmarks for each section:

```python
import pypdf

reader = pypdf.PdfReader("merged.pdf")
writer = pypdf.PdfWriter()
writer.append(reader)

# Add bookmarks (page indices are 0-based here)
writer.add_outline_item("Introduction", 0)
writer.add_outline_item("Chapter 1", 2)
writer.add_outline_item("Chapter 2", 15)
writer.add_outline_item("Appendix", 42)

with open("merged-with-bookmarks.pdf", "wb") as f:
    writer.write(f)
```

Nested bookmarks (sub-sections) use the `parent` parameter:

```python
ch1 = writer.add_outline_item("Chapter 1", 2)
writer.add_outline_item("1.1 Background", 3, parent=ch1)
writer.add_outline_item("1.2 Methods", 7, parent=ch1)
```

## Splitting a PDF into individual pages

To extract every page as its own file:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py --split original.pdf
```

This creates `original-page-001.pdf`, `original-page-002.pdf`, etc., in the current directory. The zero-padded numbering ensures correct alphabetical sort order for up to 999 pages.

For custom naming or a specific output directory, use pypdf directly:

```python
import pypdf
from pathlib import Path

reader = pypdf.PdfReader("original.pdf")
out_dir = Path("pages")
out_dir.mkdir(exist_ok=True)

for i, page in enumerate(reader.pages, 1):
    writer = pypdf.PdfWriter()
    writer.add_page(page)
    out_path = out_dir / f"page-{i:03d}.pdf"
    with open(out_path, "wb") as f:
        writer.write(f)
    print(f"Wrote {out_path}")
```

## Splitting at a page boundary

To split a 50-page PDF at page 20 (pages 1-20 in part A, 21-50 in part B):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py \
    part-a.pdf \
    "document.pdf:1-20"

python3 ${CLAUDE_SKILL_DIR}/scripts/merge.py \
    part-b.pdf \
    "document.pdf:21-50"
```

## Handling encrypted PDFs

Encrypted PDFs require the user password to open. pypdf needs it before merging:

```python
import pypdf

reader = pypdf.PdfReader("locked.pdf", password="the-password")
writer = pypdf.PdfWriter()
writer.append(reader)

# The output will NOT be encrypted by default
with open("unlocked.pdf", "wb") as f:
    writer.write(f)
```

If you need to merge an encrypted PDF without stripping its encryption in the output, this is not reliably supported by `pypdf` alone — inform the user.

## Preserving metadata

By default `pypdf` does not copy metadata from the input files to the merged output. To copy metadata from the first input file:

```python
import pypdf

reader = pypdf.PdfReader("first.pdf")
writer = pypdf.PdfWriter()
# ... append pages ...
writer.add_metadata(reader.metadata)

with open("merged.pdf", "wb") as f:
    writer.write(f)
```

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'pypdf'` | Library not installed | `pip install pypdf` |
| `FileNotFoundError` | Input file path wrong | Verify each path with `ls` |
| `pypdf.errors.FileNotDecryptedError` | Encrypted input | Provide password as shown above |
| Output PDF is larger than expected | Duplicate embedded fonts/images | Normal for merging unrelated PDFs; not fixable without re-distilling |
| Bookmarks missing in merged output | Source bookmarks not copied | Copy them explicitly with `writer.add_outline_item` |
