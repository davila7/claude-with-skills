# PDF Form Filling Reference

This reference covers form filling in detail. Read it when the user asks to fill a PDF form, set form fields, complete a PDF, or flatten a filled form.

## How PDF forms work

PDF forms store interactive fields (text boxes, checkboxes, radio buttons, dropdowns) in a data structure called the AcroForm. `pypdf` can read and write AcroForm fields without re-rendering the PDF. The visual appearance updates when the PDF is opened in a viewer that supports AcroForms — most modern PDF readers do.

## Listing available form fields

Before filling a form, identify the field names. Field names in PDFs are arbitrary strings set by whoever created the form — they are often abbreviated or use internal naming conventions.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py input.pdf --list-fields
```

This prints every field name, its type, and its current value. Example output:

```
Field: first_name    Type: /Tx    Value: (empty)
Field: last_name     Type: /Tx    Value: (empty)
Field: dob           Type: /Tx    Value: (empty)
Field: agree_terms   Type: /Btn   Value: /Off
Field: plan          Type: /Ch    Value: /option_a
```

Field types: `/Tx` = text box, `/Btn` = button (checkbox or radio), `/Ch` = choice (dropdown or list).

## Filling text fields

Pass `field=value` pairs as arguments:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py \
    input.pdf \
    output.pdf \
    first_name="Jane" \
    last_name="Smith" \
    dob="1990-04-15"
```

Field names with spaces must be quoted. Values with spaces must also be quoted:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py \
    form.pdf \
    filled.pdf \
    "company name"="Acme Corp" \
    "job title"="Senior Engineer"
```

## Filling checkboxes

Checkbox fields use `/Btn` type. The on-value is typically `/Yes` or `/On` but varies by PDF. Use `--list-fields` to confirm the exact on-value:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py \
    form.pdf \
    filled.pdf \
    agree_terms=/Yes
```

To uncheck: use `/Off`.

If the checkbox does not respond to `/Yes`, try the exact on-value reported by `--list-fields`. Some PDFs use custom values like `/1` or `/Checked`.

## Filling radio buttons

Radio button groups share a field name. Each button in the group has a distinct export value. List the fields first to see the available values:

```
Field: subscription_plan   Type: /Btn   Value: /monthly   Options: /monthly /annual /lifetime
```

Set the value to one of the export values:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py \
    form.pdf \
    filled.pdf \
    subscription_plan=/annual
```

## Filling dropdowns and list boxes

Choice fields (`/Ch` type) accept any value that is in the field's option list. `--list-fields` shows the current value but not always the full option list. If you need the full list, use `pypdf` directly:

```python
import pypdf

reader = pypdf.PdfReader("form.pdf")
fields = reader.get_fields()
for name, field in fields.items():
    if field.get("/FT") == "/Ch":
        print(f"{name}: options = {field.get('/Opt', [])}")
```

## Flattening a filled form

Flattening converts the interactive form fields into static content — the values are burned into the page and the fields can no longer be edited. This is required before printing or archiving.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_form.py \
    form.pdf \
    filled-flat.pdf \
    --flatten \
    first_name="Jane" \
    last_name="Smith"
```

Note: `pypdf` flattening support varies by PDF. For complex forms with non-standard field rendering, the flattened output may not look identical to the interactive version. Recommend the user open the output in a PDF viewer to verify before distributing.

## Filling forms with pypdf directly

If the script does not cover your case, fill fields directly:

```python
import pypdf

reader = pypdf.PdfReader("form.pdf")
writer = pypdf.PdfWriter()

writer.append(reader)
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "agree_terms": "/Yes",
    },
    auto_regenerate=False,
)

with open("filled.pdf", "wb") as f:
    writer.write(f)
```

`auto_regenerate=False` tells viewers not to regenerate appearance streams — required for some PDF viewers to display the filled values correctly.

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'pypdf'` | Library not installed | `pip install pypdf` |
| Field filled but not visible in viewer | Viewer regenerating appearance | Set `auto_regenerate=False` and re-save |
| `KeyError: 'field_name'` | Field name does not exist | Run `--list-fields` to confirm exact names |
| Checkbox stays unchecked | Wrong on-value | Check `--list-fields` output for the correct value |
| Encrypted form | PDF is read-only | Cannot fill without the owner password |
