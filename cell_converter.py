"""
Cell value conversion utilities.

Provides common logic for converting cell values based on their openpyxl data types.
Used by both Table and Object conversion modes.
"""

from typing import Any
import logging
from datetime import datetime, date
from decimal import Decimal

from models import Cell

logger = logging.getLogger(__name__)


def convert_cell_value(cell: Cell) -> Any:
    """
    Convert cell value to JSON-serializable format based on data_type.
    
    Handles all openpyxl data types:
    - 's' (string): converted to str
    - 'n' (number): Decimal converted to float, others as-is
    - 'd' (date): datetime/date converted to ISO format string
    - 'b' (boolean): converted to bool
    - 'f' (formula): converted to str
    - 'e' (error): converted to str
    - None (empty): returns None
    
    If conversion fails, logs warning and returns value as string.
    
    Args:
        cell: Cell object with data_type and value from openpyxl
        
    Returns:
        Converted value (str, int, float, bool, None) - JSON serializable
        
    Raises:
        Does not raise exceptions; logs warnings and converts to string on error
    """
    if cell.data_type is None or cell.value is None:
        return None
    
    try:
        # Boolean type
        if cell.data_type == 'b':
            return bool(cell.value)
        
        # Number type - convert Decimal to float
        elif cell.data_type == 'n':
            return float(cell.value) if isinstance(cell.value, Decimal) else cell.value
        
        # Date type - convert to ISO format string
        elif cell.data_type == 'd':
            return cell.value.isoformat() if isinstance(cell.value, (datetime, date)) else str(cell.value)
        
        # String, formula, and error types - convert to string
        elif cell.data_type in ('s', 'f', 'e'):
            return str(cell.value)
        
        # Unknown type - convert to string
        else:
            logger.warning(f"Unknown data_type '{cell.data_type}' for value {cell.value}, converting to string")
            return str(cell.value)
    
    except Exception as e:
        logger.warning(f"Error converting cell value {cell.value} with data_type '{cell.data_type}': {str(e)}")
        return str(cell.value) if cell.value is not None else None
