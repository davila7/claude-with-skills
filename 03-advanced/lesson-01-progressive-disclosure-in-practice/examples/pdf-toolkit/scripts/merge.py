#!/usr/bin/env python3
"""Merge multiple PDF files into one, or split a PDF into individual pages.

Usage:
    merge.py <output.pdf> <input1.pdf> [<input2.pdf> ...] [page-range options]
    merge.py --split <input.pdf>

Arguments:
    output.pdf      Path for the merged output file.
    input.pdf       One or more input PDFs. Append :RANGE to include only
                    specific pages from that file (e.g. chapter.pdf:2-15).

Page range formats (appended after colon):
    file.pdf:3      Page 3 only (1-indexed)
    file.pdf:2-8    Pages 2 through 8 inclusive
    file.pdf:1,4,7  Pages 1, 4, and 7
    file.pdf:5-     Page 5 through the last page

Options:
    --split         Split a single PDF into individual pages instead of merging.
                    Creates <basename>-page-NNN.pdf files in the current directory.

Examples:
    merge.py combined.pdf part1.pdf part2.pdf part3.pdf
    merge.py report.pdf cover.pdf "body.pdf:2-15" appendix.pdf
    merge.py extract.pdf "source.pdf:1,3,5"
    merge.py --split large-document.pdf
"""

import sys
import argparse
from pathlib import Path


def parse_input_spec(spec):
    """Parse 'filepath:range' into (path_str, range_str_or_None)."""
    # Find the last colon that is preceded by something that looks like a file extension
    # to avoid splitting Windows drive letters (C:\...).
    # Strategy: split on ':' from the right, but only if the left part is an existing file
    # or if the right part looks like a page range (digits, commas, hyphens).
    if ":" not in spec:
        return spec, None

    # Try splitting on the last colon
    left, right = spec.rsplit(":", 1)

    # If the right side looks like a page range (only digits, commas, hyphens), accept it
    import re
    if re.fullmatch(r"[\d,\-]+", right):
        return left, right

    # Otherwise treat the whole thing as a path (no page range)
    return spec, None


def parse_page_range(range_str, total_pages):
    """Parse a page range string and return sorted 0-based page indices."""
    if range_str is None:
        return list(range(total_pages))

    indices = set()
    parts = range_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            segs = part.split("-", 1)
            start_s, end_s = segs[0].strip(), segs[1].strip()
            start = int(start_s) if start_s else 1
            end = int(end_s) if end_s else total_pages
            if start < 1 or end > total_pages or start > end:
                raise ValueError(
                    f"range '{part}' is out of bounds (document has {total_pages} pages)"
                )
            for p in range(start, end + 1):
                indices.add(p - 1)
        else:
            p = int(part)
            if p < 1 or p > total_pages:
                raise ValueError(
                    f"page {p} is out of bounds (document has {total_pages} pages)"
                )
            indices.add(p - 1)

    return sorted(indices)


def split_pdf(input_path, reader):
    """Split a PDF into individual page files in the current directory."""
    total = len(reader.pages)
    if total == 0:
        print("Error: the PDF has no pages.", file=sys.stderr)
        sys.exit(1)

    stem = input_path.stem
    pad = len(str(total))

    import pypdf
    for i, page in enumerate(reader.pages, 1):
        writer = pypdf.PdfWriter()
        writer.add_page(page)
        out_name = f"{stem}-page-{i:0{pad}d}.pdf"
        out_path = Path(out_name)
        with open(out_path, "wb") as f:
            writer.write(f)
        print(f"  {out_path}")

    print(f"\nSplit {total} pages from '{input_path.name}' into {total} files.")


def main():
    parser = argparse.ArgumentParser(
        description="Merge PDF files or split a PDF into individual pages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="Split a single PDF into individual page files",
    )
    parser.add_argument(
        "files",
        nargs="+",
        metavar="file",
        help="For merge: output.pdf input1.pdf [input2.pdf ...]. "
             "For --split: input.pdf",
    )
    args = parser.parse_args()

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

    if args.split:
        # Split mode: exactly one input file
        if len(args.files) != 1:
            print(
                "Error: --split requires exactly one input file.",
                file=sys.stderr,
            )
            sys.exit(1)
        input_path = Path(args.files[0])
        if not input_path.exists():
            print(f"Error: file not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        try:
            reader = pypdf.PdfReader(str(input_path))
        except Exception as exc:
            print(f"Error opening '{input_path}': {exc}", file=sys.stderr)
            sys.exit(1)
        split_pdf(input_path, reader)
        return

    # Merge mode: first file is output, rest are inputs
    if len(args.files) < 2:
        print(
            "Error: merge mode requires an output path and at least one input file.\n"
            "Usage: merge.py <output.pdf> <input1.pdf> [<input2.pdf> ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = Path(args.files[0])
    input_specs = args.files[1:]

    writer = pypdf.PdfWriter()
    total_pages_added = 0

    for spec in input_specs:
        file_path_str, range_str = parse_input_spec(spec)
        input_path = Path(file_path_str)

        if not input_path.exists():
            print(f"Error: file not found: {input_path}", file=sys.stderr)
            sys.exit(1)

        try:
            reader = pypdf.PdfReader(str(input_path))
        except pypdf.errors.FileNotDecryptedError:
            print(
                f"Error: '{input_path}' is encrypted. "
                "Provide a password to open it.",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as exc:
            print(f"Error opening '{input_path}': {exc}", file=sys.stderr)
            sys.exit(1)

        total_pages = len(reader.pages)
        try:
            page_indices = parse_page_range(range_str, total_pages)
        except ValueError as exc:
            print(f"Error in '{spec}': {exc}", file=sys.stderr)
            sys.exit(1)

        for idx in page_indices:
            writer.add_page(reader.pages[idx])
            total_pages_added += 1

        range_desc = f":{range_str}" if range_str else " (all pages)"
        print(f"  Added {len(page_indices)} page(s) from '{input_path.name}'{range_desc}")

    if total_pages_added == 0:
        print("Error: no pages were added. Check input files and page ranges.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(output_path, "wb") as f:
            writer.write(f)
    except OSError as exc:
        print(f"Error writing output: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nMerged {total_pages_added} pages into: {output_path.absolute()}")


if __name__ == "__main__":
    main()
