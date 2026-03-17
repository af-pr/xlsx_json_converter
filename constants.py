"""
Constants and default configuration for the XLSX to JSON converter.
"""

from pathlib import Path

# Path configuration
DEFAULT_SOURCE_DIR = Path("sources")
DEFAULT_SOURCE_FILENAME = "source.xlsx"
DEFAULT_OUTPUT_DIR = Path("output")
DEFAULT_OUTPUT_FILENAME = "output.json" # TODO: review if this is correct. If there is already an output.json we should create output(<n>).json. Maybe we can use 'output' and JSON_EXTENSION

# File extensions
XLSX_EXTENSION = ".xlsx"
JSON_EXTENSION = ".json"

# JSON formatting
JSON_INDENT = 2
JSON_ENSURE_ASCII = False

# Error messages
MSG_FILE_NOT_FOUND = "File not found: {}"
MSG_INVALID_FORMAT = "Invalid XLSX format: {}"
MSG_INVALID_INPUT = "Invalid input: {}"
MSG_FILE_EXISTS = "Output file already exists: {}"
