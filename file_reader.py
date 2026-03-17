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
from exceptions import FileNotFoundError, ReadFileError


def read_file(path_input: str = "") -> bytes:
    """
    Read XLSX file and return raw binary content.
    
    Args:
        path_input: Full path, filename in default directory, or empty string (uses default: sources/source.xlsx)
        
    Returns:
        Binary file content as bytes
        
    Raises:
        FileNotFoundError: If file does not exist or path points to a directory
        ReadFileError: If file cannot be read due to permission errors or other I/O issues
    """

    path = _validate_input_as_path(path_input)

    if not path.is_file():
        raise FileNotFoundError(f"File not found or it is a directory: {path}")
    
    try:
        with path.open("rb") as f:
            return f.read()
    except PermissionError:
        raise ReadFileError(f"Permission denied reading file: {path}")
    except IsADirectoryError:
        raise ReadFileError(f"Path is a directory, not a file: {path}")
    except (OSError, IOError) as e:
        raise ReadFileError(f"Cannot read file: {path} - {str(e)}")
    except Exception as e: # Fallback
        raise ReadFileError(f"Unexpected error reading file: {path} - {str(e)}")

def _validate_input_as_path(path_input: str = "") -> Path:
    """
    Validate user input and resolve to actual file path.
    
    Input resolution rules:
    - Empty string: Returns default (sources/source.xlsx)
    - Filename only: Returns sources/{filename}
    - Full path (contains / or \\): Returns path as-is
    
    Automatically appends .xlsx extension if input doesn't have it (case-insensitive check).
    
    Args:
        path_input: Filename, full path, or empty string
        
    Returns:
        Resolved Path object pointing to XLSX file
    """

    if path_input == "" or path_input is None:
        path = DEFAULT_SOURCE_DIR / DEFAULT_SOURCE_FILENAME
    elif '/' in path_input or '\\' in path_input:
        path =  Path(path_input)
    else:
        path = DEFAULT_SOURCE_DIR / path_input

    # If the input doesn't have .xlsx extension, we add it automatically
    if XLSX_EXTENSION.lower() not in path.suffix.lower():
        path = path.with_suffix(XLSX_EXTENSION)
    
    return path
