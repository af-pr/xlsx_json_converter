
# XLSX to JSON Converter

Python library for converting XLSX files to JSON format with type preservation and validation.

## Features

- ✅ Converts XLSX files to JSON format
- ✅ Preserves cell data type information from source XLSX
- ✅ Type consistency validation per column (non-blocking warnings)
- ✅ Automatic collision avoidance for output filenames
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

You will be prompted for:
1. Source XLSX filename (default: `source.xlsx`)
2. Output JSON filename (default: `output.json`)

### As Python Library

```python
from xlsx_json_converter import Converter, json_validator

# Create converter and convert file
converter = Converter()
output_path = converter.convert("data.xlsx", "output.json")

# Optionally validate types
warnings = json_validator.validate_sheet_data(sheet_data)
for warning in warnings:
    print(f"Column '{warning.column_header}' has mixed types")
```

## Project Structure

```
xlsx_json_converter/
├── main.py                  # CLI entry point
├── converter.py             # Main orchestrator class
├── file_reader.py           # XLSX file reading
├── xlsx_parser.py           # XLSX parsing to SheetData
├── json_converter.py        # Serialization to JSON
├── json_validator.py        # Type consistency validation
├── file_writer.py           # JSON file writing
├── models.py                # Data structures (Cell, SheetData)
├── exceptions.py            # Custom exceptions
├── constants.py             # Configuration constants
└── __init__.py              # Package initialization
```

## Input Format Requirements

The XLSX file must follow this structure:

- **First row is ALWAYS treated as column headers**
  - If a header cell is empty, it will be auto-generated as `Column_1`, `Column_2`, etc.
  - If the entire first row is empty, all headers will be auto-generated
  - WARNING! If the first row is data it will still be processed as headers
- **Rows 2 onwards**: Actual data
```

## Output Format

The generated JSON preserves cell type information:

```json
{
  "sheets": [
    {
      "name": "Sheet1",
      "headers": ["Date", "Amount", "Description"],
      "rows": [
        [
          {"data_type": "d", "value": "2026-01-15"},
          {"data_type": "n", "value": 150.50},
          {"data_type": "s", "value": "Payment"}
        ]
      ]
    }
  ]
}
```

Cell data types:
- `'s'` - String
- `'n'` - Number
- `'d'` - Date
- `'b'` - Boolean
- `'f'` - Formula
- `'e'` - Error
- `None` - Empty cell

## License

[MIT](LICENSE)

## Author

Created by af-pr - https://github.com/af-pr
