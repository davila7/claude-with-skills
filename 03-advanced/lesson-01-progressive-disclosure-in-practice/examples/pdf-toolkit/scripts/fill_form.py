#!/usr/bin/env python3
"""Fill fields in a PDF form.

Usage:
    fill_form.py <input.pdf> [--list-fields]
    fill_form.py <input.pdf> <output.pdf> [--flatten] field=value ...

Arguments:
    input.pdf       Path to the PDF form to fill.
    output.pdf      Path for the filled output PDF.
    field=value     One or more field assignments. Field names with spaces must
                    be quoted. Values with spaces must also be quoted.

Options:
    --list-fields   Print all form fields, their types, and current values,
                    then exit without writing any output.
    --flatten       Flatten the form after filling (makes fields non-editable).

Examples:
    fill_form.py application.pdf --list-fields
    fill_form.py application.pdf filled.pdf first_name=Jane last_name=Smith
    fill_form.py application.pdf flat.pdf --flatten agree_terms=/Yes name=Jane
"""

import sys
import argparse
from pathlib import Path


# Map AcroForm field type codes to readable names
FIELD_TYPE_NAMES = {
    "/Tx": "text",
    "/Btn": "button (checkbox/radio)",
    "/Ch": "choice (dropdown/list)",
    "/Sig": "signature",
}


def list_fields(reader):
    """Print all form fields to stdout and return."""
    fields = reader.get_fields()
    if not fields:
        print("No form fields found in this PDF.")
        return

    print(f"{'Field name':<40} {'Type':<28} {'Current value'}")
    print("-" * 90)
    for name, field in sorted(fields.items()):
        ftype_code = field.get("/FT", "(unknown)")
        ftype = FIELD_TYPE_NAMES.get(ftype_code, ftype_code)
        value = field.get("/V", "(empty)")
        if value is None:
            value = "(empty)"
        print(f"{name:<40} {ftype:<28} {value}")


def parse_field_assignments(tokens):
    """Parse a list of 'field=value' strings into a dict."""
    assignments = {}
    for token in tokens:
        if "=" not in token:
            print(
                f"Error: argument '{token}' is not a valid field assignment. "
                "Use the format: field_name=value",
                file=sys.stderr,
            )
            sys.exit(1)
        name, value = token.split("=", 1)
        name = name.strip()
        if not name:
            print(
                f"Error: empty field name in assignment '{token}'.",
                file=sys.stderr,
            )
            sys.exit(1)
        assignments[name] = value
    return assignments


def main():
    parser = argparse.ArgumentParser(
        description="Fill fields in a PDF form.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", help="Path to the input PDF form")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Path for the filled output PDF (omit when using --list-fields)",
    )
    parser.add_argument(
        "--list-fields",
        action="store_true",
        help="List all form fields and exit",
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Flatten the form after filling (fields become non-editable)",
    )
    parser.add_argument(
        "assignments",
        nargs="*",
        metavar="field=value",
        help="Field assignments",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

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

    try:
        reader = pypdf.PdfReader(str(input_path))
    except pypdf.errors.FileNotDecryptedError:
        print(
            f"Error: '{input_path}' is encrypted. Provide a password to open it.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as exc:
        print(f"Error opening PDF: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.list_fields:
        list_fields(reader)
        return

    if args.output is None:
        print(
            "Error: an output path is required when filling fields. "
            "Use --list-fields to only inspect the form.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = Path(args.output)

    if not args.assignments:
        print(
            "Warning: no field assignments provided. "
            "The output PDF will be a copy of the input.",
            file=sys.stderr,
        )

    field_values = parse_field_assignments(args.assignments)

    # Verify that all requested field names exist
    available_fields = reader.get_fields() or {}
    unknown = [name for name in field_values if name not in available_fields]
    if unknown:
        print(
            f"Error: the following fields were not found in the form: {unknown}\n"
            "Run with --list-fields to see available field names.",
            file=sys.stderr,
        )
        sys.exit(1)

    writer = pypdf.PdfWriter()
    writer.append(reader)

    if field_values:
        for page in writer.pages:
            writer.update_page_form_field_values(
                page,
                field_values,
                auto_regenerate=False,
            )

    if args.flatten:
        # Flattening: mark all fields as read-only and remove interactivity
        # pypdf supports this via the flatten() method on the writer
        if hasattr(writer, "flatten"):
            writer.flatten()
        else:
            # Fallback for older pypdf versions: set the read-only flag on each field
            if "/AcroForm" in writer._root_object:
                acroform = writer._root_object["/AcroForm"]
                if "/Fields" in acroform:
                    for field_ref in acroform["/Fields"]:
                        field = field_ref.get_object()
                        # Bit 1 of /Ff is the ReadOnly flag
                        existing_ff = int(field.get("/Ff", 0))
                        field[pypdf.generic.NameObject("/Ff")] = (
                            pypdf.generic.NumberObject(existing_ff | 1)
                        )

    try:
        with open(output_path, "wb") as f:
            writer.write(f)
    except OSError as exc:
        print(f"Error writing output: {exc}", file=sys.stderr)
        sys.exit(1)

    filled_count = len(field_values)
    flatten_note = " (flattened)" if args.flatten else ""
    print(
        f"Filled {filled_count} field(s){flatten_note}. "
        f"Output written to: {output_path.absolute()}"
    )


if __name__ == "__main__":
    main()
