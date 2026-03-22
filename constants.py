"""
Constants and default configuration for the XLSX to JSON converter.
"""

from pathlib import Path
from enum import Enum

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Path configuration
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "sources"
DEFAULT_SOURCE_FILENAME = "source.xlsx"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_OUTPUT_FILENAME_START = "output"

# File extensions
XLSX_EXTENSION = ".xlsx"
JSON_EXTENSION = ".json"

# JSON formatting
JSON_INDENT = 2
JSON_ENSURE_ASCII = False

# XLSX Parser configuration
HEADER_ROW_INDEX = 1
DATA_START_ROW = 2
AUTO_HEADER_PREFIX = "Column_"


class JsonTableKeys(Enum):
    """JSON output keys for table-format conversion."""
    SHEETS = "sheets"
    NAME = "name"
    HEADERS = "headers"
    ROWS = "rows"
    DATA_TYPE = "data_type"
    VALUE = "value"
    CONVERSION_ERROR = "conversion_error"


class JsonObjectKeys(Enum):
    """JSON output keys for object-format conversion."""
    SHEET = "sheet"
    CONTENT = "content"
