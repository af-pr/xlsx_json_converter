"""
XLSX to JSON Converter

A professional Python library for converting XLSX files to JSON format.

Features:
- Preserves cell type information from source XLSX
- Detects and reports type inconsistencies per column
- Supports multiple sheets
- Auto-generates headers if source doesn't have them
- Avoids filename collisions automatically

Can be used as a CLI tool or imported as a library:

    from xlsx_json_converter import Converter, json_validator
    
    converter = Converter()
    output_path = converter.convert("data.xlsx", "output.json")
    
    # Get type validation warnings if needed
    warnings = json_validator.validate_sheet_data(sheet_data)
    for w in warnings:
        print(f"Column {w.column_header}: {w.type_distribution}")

Or run as CLI:
    python main.py
"""

from converter import Converter
from exceptions import (
    ConverterError,
    FileNotFoundError,
    InvalidFormatError,
    InvalidInputError,
    ReadFileError,
    WriteFileError,
)
import json_validator

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

__all__ = [
    "Converter",
    "ConverterError",
    "FileNotFoundError",
    "InvalidFormatError",
    "InvalidInputError",
    "ReadFileError",
    "WriteFileError",
    "json_validator",
]
