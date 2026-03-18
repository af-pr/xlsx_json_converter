"""
File writing module for saving JSON output.

Handles:
- Output filename validation
- JSON extension management
- Output directory creation
- Collision avoidance (output.json → output(2).json → output(3).json)
- File writing with error handling
"""

from pathlib import Path

from constants import DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FILENAME, JSON_EXTENSION
from exceptions import WriteFileError, InvalidInputError


def write(content: str, filename: str = "") -> Path:
    """
    Write JSON content to output file. If no filename provided, uses default output filename.
    If using default filename, ensures no existing files are overwritten.
    
    WARNING: if providing a custom filename, it will be used as-is (with .json extension auto-appended if missing)
    and will overwrite existing files without warning.
    
    Args:
        content: JSON string to write
        filename: Output filename (no path allowed)
        
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
    Returns a path to a valid output file. Ensures no path separators, appends .json if missing, and resolves to a safe filename in the output directory.
    Args:
        filename: Desired output filename (no path) 
    Returns:    
        Path to a valid output file (guaranteed not to overwrite existing files if using default name)
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
    Find a safe default filename that doesn't collide with existing files.
    
    If output.json exists, tries output(2).json, output(3).json, etc.
    
    Args:
        None
        
    Returns:
        str: Filename guaranteed not to exist
    """
    
    # Checking if default output file already exists
    if not (DEFAULT_OUTPUT_DIR / DEFAULT_OUTPUT_FILENAME).exists():
        filename = DEFAULT_OUTPUT_FILENAME
    # If it exists, we need to find a new name by appending (n) before the extension
    else: 
        base_name = DEFAULT_OUTPUT_FILENAME[:-len(JSON_EXTENSION)]
        n = 2
        filename = (base_name + JSON_EXTENSION)
        while (DEFAULT_OUTPUT_DIR / filename).exists():
            n += 1
            filename = f"{base_name}({n}){JSON_EXTENSION}"
    
    return filename
