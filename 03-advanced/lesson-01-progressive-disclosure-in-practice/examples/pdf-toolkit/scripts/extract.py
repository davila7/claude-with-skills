#!/usr/bin/env python3
"""Extract text from a PDF file.

Usage:
    extract.py <input.pdf> [--pages RANGE]

Arguments:
    input.pdf       Path to the PDF file to extract text from.

Options:
    --pages RANGE   Page range to extract. Formats:
                      3         single page
                      2-5       inclusive range
                      1,3,7     specific pages
                      all       all pages (default)

Examples:
    extract.py report.pdf
    extract.py report.pdf --pages 1-4
    extract.py report.pdf --pages 3
    extract.py report.pdf --pages 1,5,9
"""

import sys
import argparse
from pathlib import Path


def parse_page_range(page_range_str, total_pages):
    """Parse a page range string and return a list of 0-based page indices."""
    if page_range_str is None or page_range_str.lower() == "all":
        return list(range(total_pages))

    indices = set()
    parts = page_range_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            segments = part.split("-", 1)
            start_s, end_s = segments[0].strip(), segments[1].strip()
            start = int(start_s) if start_s else 1
            end = int(end_s) if end_s else total_pages
            if start < 1 or end > total_pages:
                print(
                    f"Error: page range {part} is out of bounds "
                    f"(document has {total_pages} pages).",
                    file=sys.stderr,
                )
                sys.exit(1)
            for p in range(start, end + 1):
                indices.add(p - 1)  # convert to 0-based
        else:
            p = int(part)
            if p < 1 or p > total_pages:
                print(
                    f"Error: page {p} is out of bounds "
                    f"(document has {total_pages} pages).",
                    file=sys.stderr,
                )
                sys.exit(1)
            indices.add(p - 1)  # convert to 0-based

    return sorted(indices)


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", help="Path to the PDF file")
    parser.add_argument(
        "--pages",
        default=None,
        metavar="RANGE",
        help="Page range to extract (e.g. 1-5, 3, 1,4,7, all). Default: all.",
    )
    args = parser.parse_args()

    # Check that the input file exists before attempting to import pypdf
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    if not input_path.is_file():
        print(f"Error: not a file: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Import pypdf with a helpful error message if it is not installed
    try:
        import pypdf
    except ImportError:
        print(
            "Error: the 'pypdf' library is not installed.\n"
            "Install it with:\n"
            "    pip install pypdf",
            file=sys.stderr,
        )
        sys.exit(1)

    # Open the PDF
    try:
        reader = pypdf.PdfReader(str(input_path))
    except pypdf.errors.FileNotDecryptedError:
        print(
            f"Error: '{input_path}' is encrypted. "
            "Open it with a password:\n"
            "    pypdf.PdfReader('file.pdf', password='your-password')",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as exc:
        print(f"Error opening PDF: {exc}", file=sys.stderr)
        sys.exit(1)

    total_pages = len(reader.pages)
    if total_pages == 0:
        print("Error: the PDF has no pages.", file=sys.stderr)
        sys.exit(1)

    # Parse the requested page range
    try:
        page_indices = parse_page_range(args.pages, total_pages)
    except ValueError as exc:
        print(f"Error: invalid page range '{args.pages}': {exc}", file=sys.stderr)
        sys.exit(1)

    if not page_indices:
        print("Error: the specified page range produced no pages.", file=sys.stderr)
        sys.exit(1)

    # Extract and print text
    extracted_any = False
    for idx in page_indices:
        page = reader.pages[idx]
        text = page.extract_text() or ""
        print(f"--- Page {idx + 1} ---")
        if text.strip():
            print(text)
            extracted_any = True
        else:
            print("(no extractable text on this page)")

    if not extracted_any:
        print(
            "\nNote: no text was extracted from any page. "
            "This may be a scanned PDF that contains images rather than embedded text. "
            "pypdf cannot perform OCR. "
            "See the extraction reference for OCR options using pytesseract.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
