"""
JSON serialization module for SheetData objects.

Converts SheetData structures to JSON format.
"""

from typing import List, Any
import json
from datetime import datetime, date
from decimal import Decimal

from models import SheetData, Cell
from exceptions import ConverterError
from constants import JSON_INDENT, JSON_ENSURE_ASCII


def convert_sheet_data_to_json(sheet_data_list: List[SheetData]) -> str:
    """
    Convert SheetData objects to formatted JSON string. It parses the original data types and handles non-JSON-serializable types with a custom encoder.
    If a type cannot be converted, it will be converted to string and a warning will be written to the console.
    
    Args:
        sheet_data_list: List of SheetData objects to convert
        
    Returns:
        Formatted JSON string
        
    Raises:
        ConverterError: If serialization fails
    """
    #- Handles non-JSON-serializable types (datetime, Decimal) via custom encoder.
    #- If a type cannot be converted, it will be converted to string and a WARN will be written to the console.
    #- The json should keep the original data types as much as possible, this could be necessary for downstream processing.
    #- TODO: improvement - instead of writing to console, should we return the warnings? Or create a logging mechanism?
    pass


def _custom_json_encoder(obj: Any) -> Any:
    """
    Handle JSON serialization of non-standard types.
    
    Converts datetime/date to ISO format strings, Decimal to float,
    and bytes to base64 encoded strings.
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serializable representation
        
    Raises:
        TypeError: If type cannot be serialized
    """
    
    #- Converts:
    #- datetime/date → ISO format string? Timestamp?
    #- Decimal → float
    #- bytes → base64 string
    pass