
# XLSX to JSON Converter

Python library for converting XLSX files to JSON format with type preservation and validation.

## Features

- ✅ Converts XLSX files to JSON format with **dual conversion modes**
- ✅ **Table Mode**: Nested structure with headers, rows, and type metadata
- ✅ **Object Mode**: Flat object structures where each row maps to an object with headers as keys
- ✅ Preserves cell data type information from source XLSX (Table mode only)
- ✅ Type consistency validation per column (non-blocking warnings)
- ✅ Timestamped output filenames to avoid collisions (e.g. `output-20260318-101533722062.json`)
- ✅ Usable as CLI tool or importable Python library

## Installation

### Requirements

- Python 3.8+
- openpyxl (for XLSX parsing)

### Setup

```bash
pip install -r requirements.txt
```

## Usage

### As CLI Tool

```bash
python main.py
```

The CLI will:
1. Prompt for source XLSX filename (default: `source.xlsx` in `sources/` directory)
2. Prompt for output JSON filename (default: auto-generated timestamp like `output-20260318-101533722062.json`)
3. Prompt for conversion mode: `table` or `object` (default: `table`)
4. Perform conversion and display results
5. **Automatically validate type consistency** across columns and display any warnings

Example conversion mode selection:
```
Enter source filename: source.xlsx
Enter output filename: 
Conversion modes:
  'table': Nested structure with headers, rows, and metadata
  'object': Flat object structure (each row as an object)
Enter conversion mode [table(t)/object(o)] [default: table]: object

✅ Conversion successful!

Output file created:
  output/output-20260318-101533722062.json
```

Example output with type inconsistencies:
```
✅ Conversion successful!

Output file created:
  output/output-20260318-101533722062.json

⚠️  Type inconsistencies found in 2 column(s):

  -- Column 'Amount' (index 3):
    - 'n': rows [0, 1, 2]
    - 's': rows [3, 4, ... (+10 more)]

  -- Column 'Date' (index 0):
    - 'd': rows [0, 1]
    - 's': rows [2]
```

### As Python Library

```python
from converter import Converter

# Create converter and convert file with table or object mode
converter = Converter()
output_path, validation_results = converter.convert("source.xlsx", "output", "table")

# Or use Object mode
output_path, validation_results = converter.convert("source.xlsx", "output.json", "object")

# Check validation results
for result in validation_results:
    if not result.validated:
        print(f"Column '{result.column_header}' has mixed types:")
        for data_type, rows in result.type_distribution.items():
            print(f"  {data_type}: {rows}")
```

## Project Structure

```
xlsx_json_converter/
├── main.py                      # CLI entry point
├── converter.py                 # Main orchestrator class
├── file_reader.py               # XLSX file reading
├── xlsx_parser.py               # XLSX parsing to SheetData
├── json_table_converter.py      # Table mode: JSON with type metadata
├── json_object_converter.py     # Object mode: Flat object structures
├── data_validator.py            # Type consistency validation
├── file_writer.py               # JSON file writing
├── models.py                    # Data structures (Cell, SheetData)
├── exceptions.py                # Custom exceptions
├── constants.py                 # Configuration constants
├── requirements.txt             # Pip dependencies
└── README.md                    # This file
```

## Input Format Requirements

The XLSX file must follow this structure:

- **First row is ALWAYS treated as column headers**
  - If a header cell is empty, it will be auto-generated as `Column_1`, `Column_2`, etc.
  - If the entire first row is empty, all headers will be auto-generated
  - WARNING! If the first row is data it will still be processed as headers
- **Rows 2 onwards**: Actual data

### Header Names for Object Mode

When using **Object mode**, headers are automatically transformed into object attribute names. The transformation rules are:

1. **Remove non-alphanumeric characters**: All characters except letters, numbers, and the Unicode character class are removed
   - Example: `"User-ID"` → `"UserID"`

2. **Convert to camelCase**: 
   - First word: all lowercase
   - Subsequent words: first letter uppercase, rest lowercase
   - Multiple spaces/underscores/hyphens are treated as word separators
   - Example: `"First Name"` → `"firstName"`

3. **Header uniqueness requirement**: After transformation, all headers must be **unique**. If transformation results in duplicate attribute names, the conversion will fail with an error.
   - Example that FAILS: Headers `"firstName"` and `"First-Name"` both transform to `"firstName"` → Error!
   - Example that FAILS: Headers `"first name"` and `"First Name"` both transform to `"firstName"` → Error!
```

## Output Formats

The converter supports two output formats depending on the chosen conversion mode:

### Table Mode (Default)

Table mode is optimized for preserving all type information and metadata. Each cell includes type and conversion error information.

**Structure:**
```json
{
  "sheets": [
    {
      "name": "Sheet1",
      "headers": ["Date", "Amount", "Description"],
      "rows": [
        [
          {"data_type": "d", "value": "2026-01-15", "conversion_error": false},
          {"data_type": "n", "value": 150.50, "conversion_error": false},
          {"data_type": "s", "value": "Payment", "conversion_error": false}
        ],
        [
          {"data_type": "d", "value": "2026-01-16", "conversion_error": false},
          {"data_type": "n", "value": 250.00, "conversion_error": false},
          {"data_type": "s", "value": "Refund", "conversion_error": false}
        ]
      ]
    }
  ]
}
```

**Cell fields:**
- `data_type`: Original Excel cell type (see table below)
- `value`: Converted cell value (JSON-serializable)
- `conversion_error`: `true` if conversion failed and value was cast to string as fallback

### Object Mode

Object mode is optimized for object-oriented consumption. Each row becomes a flat object with headers as keys. Empty cells are represented as `null`.

**Structure:**
```json
[
  {
    "sheet": "Sheet1",
    "content": [
      {
        "date": "2026-01-15",
        "amount": 150.50,
        "description": "Payment"
      },
      {
        "date": "2026-01-16",
        "amount": 250.00,
        "description": "Refund"
      }
    ]
  }
]
```

**Features:**
- Headers are automatically transformed:
  - Non-alphanumeric characters removed
  - Converted to camelCase (first letter lowercase)
  - Example: `"First Name"` → `"firstName"`, `"User-ID"` → `"userId"`
- Only values are included (no type metadata)
- Empty cells are represented as `null`
- Exception thrown if header transformation results in duplicate names

### Cell Data Types

Both modes support and preserve these Excel cell types:

- `'s'` - String
- `'n'` - Number
- `'d'` - Date
- `'b'` - Boolean
- `'f'` - Formula
- `'e'` - Error
- `None` - Empty cell

## Validation

The converter automatically performs **type consistency validation** on all columns:

### How it Works

- **Per-column analysis**: Each column is analyzed to detect if all non-empty cells have the same data type
- **Empty cells**: Validation ignores empty cells to avoid false possitives
- **Non-blocking**: Validation warnings are displayed but do not stop the conversion
- **Detailed reporting**: Shows which rows have mismatched types and what types were found

### Type Validation Results

Each validated column returns a `ColumnValidationResult` containing:
- `column_index`: Position of the column (0-based)
- `column_header`: Header name
- `validated`: `true` if all cells have the same type, `false` if mixed types found
- `type_distribution`: Dict showing which rows contain each data type. If all the columns have the same type there will only be one element in the dict

Example:
```python
{
  "column_index": 3,
  "column_header": "Amount",
  "validated": false,
  "type_distribution": {
    "n": [0, 1, 2],      # Rows with numbers
    "s": [3, 4, 5, 6]    # Rows with strings (unexpected!)
  }
}
```

### When to Check Validation

If you see type warnings:
1. **Review the source XLSX**: Check if data entry is inconsistent
2. **Verify conversion**: Ensure the JSON `conversion_error` flag is `false` for important fields
3. **Clean the source**: Consider fixing the XLSX data for consistency

## License

[MIT](LICENSE)

## Author

Created by af-pr - https://github.com/af-pr
