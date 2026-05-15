---
title: "PDF Text Extraction Reference"
---

This reference covers text extraction in detail. Read it when the user asks to extract text, read content, parse a PDF, or retrieve specific pages.

## Basic extraction

The `extract.py` script wraps `pypdf` for text extraction:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py report.pdf
```

Output goes to stdout with page separators (`--- Page N ---`). Redirect to a file with:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py report.pdf > output.txt
```

## Page ranges

The `--pages` flag accepts several formats:

| Format | Meaning |
|--------|---------|
| `--pages 3` | Page 3 only (1-indexed) |
| `--pages 2-5` | Pages 2 through 5 inclusive |
| `--pages 1,3,7` | Pages 1, 3, and 7 only |
| `--pages all` | All pages (default behavior) |

Example — extract the executive summary from pages 1 through 4:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py annual-report.pdf --pages 1-4
```

## Multi-column PDFs

`pypdf` extracts text in the order it appears in the PDF's content stream, which for multi-column layouts is usually left-to-right, top-to-bottom across both columns rather than column by column. The result is often interleaved text that reads incorrectly.

For multi-column PDFs, install `pdfplumber` and use it directly:

```bash
pip install pdfplumber
python3 - <<'EOF'
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        # Extract with bounding boxes to separate columns
        left = page.within_bbox((0, 0, page.width / 2, page.height))
        right = page.within_bbox((page.width / 2, 0, page.width, page.height))
        print(f"--- Page {i} ---")
        print(left.extract_text() or "")
        print(right.extract_text() or "")
EOF
```

Adjust the column split point (`page.width / 2`) if the PDF uses an uneven two-column layout.

## Table extraction

`pypdf` does not extract tables — it extracts raw text and tables lose their structure. Use `pdfplumber` for tables:

```bash
pip install pdfplumber
python3 - <<'EOF'
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        tables = page.extract_tables()
        if tables:
            print(f"--- Page {i}: {len(tables)} table(s) ---")
            for t, table in enumerate(tables, 1):
                print(f"Table {t}:")
                for row in table:
                    print("\t".join(cell or "" for cell in row))
        else:
            print(f"--- Page {i}: no tables ---")
EOF
```

For CSV output, replace the print loop with `csv.writer`:

```python
import csv, sys, pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    writer = csv.writer(sys.stdout)
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                writer.writerow(row)
```

## Scanned PDFs (OCR limitation)

`pypdf` reads text embedded in the PDF's content stream. If the PDF was created by scanning a physical document and saving the scan as an image, there is no embedded text — `pypdf` will return empty strings for every page.

Signs the PDF is a scanned image:
- `extract.py` returns blank output or only whitespace
- The PDF file size is large relative to its apparent text content
- Selecting text in a PDF viewer selects nothing or selects in image blocks

`pypdf` cannot perform OCR. For scanned PDFs you need `pytesseract` (a wrapper for the Tesseract OCR engine):

```bash
pip install pytesseract pillow pdf2image
# Tesseract must be installed at the system level:
# macOS: brew install tesseract
# Ubuntu/Debian: sudo apt install tesseract-ocr

python3 - <<'EOF'
from pdf2image import convert_from_path
import pytesseract

pages = convert_from_path("scanned.pdf", dpi=300)
for i, image in enumerate(pages, 1):
    print(f"--- Page {i} ---")
    print(pytesseract.image_to_string(image))
EOF
```

This is significantly slower than native text extraction (seconds per page rather than milliseconds). Tell the user this before running it on a large document.

## Encrypted PDFs

`pypdf` can open password-protected PDFs if you provide the password:

```python
import pypdf

reader = pypdf.PdfReader("locked.pdf", password="the-password")
for page in reader.pages:
    print(page.extract_text())
```

If you do not have the password, `pypdf` raises `pypdf.errors.FileNotDecryptedError`. There is no way to bypass this with standard tools — inform the user.

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'pypdf'` | Library not installed | `pip install pypdf` |
| `FileNotFoundError` | Wrong path | Check the path with `ls` before running |
| `pypdf.errors.FileNotDecryptedError` | Encrypted PDF without password | Ask user for the password |
| Empty output on all pages | Scanned PDF with no embedded text | Use the OCR approach above |
| Garbled text on some pages | Encoding issue in the PDF | Try `pdfplumber` as an alternative |
