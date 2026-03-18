"""
File writing module for saving JSON output.

Handles:
- Output filename validation
- JSON extension management
- Output directory creation
- Timestamp-based filename generation (output-YYYYMMDD-HHMM.json)
- File writing with error handling
"""

from pathlib import Path
from datetime import datetime, time

from constants import DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FILENAME_START, JSON_EXTENSION
from exceptions import WriteFileError, InvalidInputError


def write(content: str, filename: str = "") -> Path:
    """
    Write JSON content to output file. If no filename provided, generates a timestamped default filename.
    
    Default filename format: output-YYYYMMDD-HHMM.json (e.g., output-20260318-1007.json)
    
    WARNING: if providing a custom filename, it will be used as-is (with .json extension auto-appended if missing)
    and will overwrite existing files without warning.
    
    Args:
        content: JSON string to write
        filename: Output filename (no path allowed), or empty for timestamped default
        
    Returns:
        Path to the written file
        
    Raises:
        InvalidInputError: If path separators in filename
        WriteFileError: If file cannot be written
    """
    # Creating output directory if it doesn't exist
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    file_path = _get_valid_path(filename)
    
    try:
        with file_path.open("w", encoding="utf-8") as f:
            f.write(content)
        return file_path
    except PermissionError:
        raise WriteFileError(f"Permission denied writing file: {file_path}") 
    except (OSError, IOError) as e:
        raise WriteFileError(f"Cannot write file: {file_path} - {str(e)}")
    except Exception as e: # Fallback
        raise WriteFileError(f"Unexpected error writing file: {file_path} - {str(e)}")



def _get_valid_path(filename: str) -> Path:
    """
    Returns a path to a valid output file. 
    
    If no filename provided, generates a timestamped default filename.
    If filename provided, ensures no path separators and appends .json if missing.
    
    Args:
        filename: Desired output filename (no path allowed), or empty for default
        
    Returns:    
        Path to a valid output file in DEFAULT_OUTPUT_DIR
        
    Raises:
        InvalidInputError: If filename contains path separators
    """
    if not filename:
        filename = _generate_default_filename()
    elif "/" in filename or "\\" in filename:
        raise InvalidInputError(f"Ouput filename contains path separators: {filename}") 
    elif not filename.lower().endswith(JSON_EXTENSION):
        filename += JSON_EXTENSION
    return DEFAULT_OUTPUT_DIR / filename


def _generate_default_filename() -> str:
    """
    Generate a timestamped default filename.
    
    Generates filename with current date and time in format:
    {DEFAULT_OUTPUT_FILENAME_START}-YYYYMMDD-HHMM.json
    
    Example: output-20260318-1007.json (March 18, 2026 at 10:07 AM)
    
    Uses leading zeros to ensure consistent length:
    - YYYY: 4 digits (year)
    - MM: 2 digits (month, 01-12)
    - DD: 2 digits (day, 01-31)
    - HH: 2 digits (hour, 00-23)
    - MM: 2 digits (minute, 00-59)
    - SS: 2 digits (second, 00-59)
    - fff: 6 digits (microsecond, 000000-999999)
    
    Args:
        None
        
    Returns:
        str: Filename with timestamp, guaranteed to be unique per microsecond
    """
    now = datetime.now()
    date_with_time = now.strftime("%Y%m%d-%H%M%S%f")
    return f"{DEFAULT_OUTPUT_FILENAME_START}-{date_with_time}{JSON_EXTENSION}"
