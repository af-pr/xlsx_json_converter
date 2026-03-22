"""
XLSX to JSON Converter

A professional Python library for converting XLSX files to JSON format.

Features:
- Preserves cell type information from source XLSX
- Detects and reports type inconsistencies per column
- Supports multiple sheets
- Treats first row as headers (auto-generates Column_N for empty cells)
- Avoids filename collisions automatically

Input Format:
- First row ALWAYS treated as column headers
- Empty header cells auto-generate as Column_1, Column_2, etc.
- Data rows start from row 2 onwards

Can be used as a CLI tool or imported as a library:

    from xlsx_json_converter import ConversionManager, data_validator
    
    manager = ConversionManager()
    output_path = manager.convert(ConversionMode.TABLE, "data.xlsx", "output.json")
    
    # Get type validation warnings if needed
    warnings = json_validator.validate_sheet_data(sheet_data)
    for w in warnings:
        print(f"Column {w.column_header}: {w.type_distribution}")

Or run as CLI:
    python main.py
"""

from conversion_manager import ConversionManager
from exceptions import (
    ConverterError,
    FileNotFoundError,
    InvalidFormatError,
    InvalidInputError,
    ReadFileError,
    WriteFileError,
)
import xlsx_json_converter.data_validator as data_validator

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
    "data_validator",
]
