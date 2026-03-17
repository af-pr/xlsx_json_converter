"""
File reading module for loading XLSX files.

Handles:
- User input validation (filename with optional path detection)
- Default path resolution (sources/ directory)
- File existence verification
- Binary file reading
"""

from pathlib import Path

from constants import DEFAULT_SOURCE_DIR, DEFAULT_SOURCE_FILENAME, XLSX_EXTENSION
from exceptions import FileNotFoundError, InvalidInputError


def read_file(user_input: str = "") -> bytes:
    """
    Read XLSX file and return raw binary content.
    
    Args:
        user_input: Filename or empty string
        
    Returns:
        Binary file content
        
    Raises:
        FileNotFoundError: If file cannot be read
    """
    #- Validate input with _validate_input
    #- Validate file exists
    #- Read file in binary mode and return content
    pass

def _validate_input(user_input: str = "") -> Path:
    """
    Validate user input and resolve to actual file path. If input is empty, use default source path.
    
    Args:
        user_input: Filename or empty string
        
    Returns:
        Resolved Path object to the XLSX file
        
    Raises:
        InvalidInputError: If path separators detected in input
        FileNotFoundError: If resolved file doesn't exist
    """

    #- Empty input → use default (sources/source.xlsx)
    #- Only filename → use default directory (sources/)
    #- If both are providadded, use as-is
    pass
