"""
Cell value conversion utilities.

Provides common logic for converting cell values based on their openpyxl data types.
Used by both Table and Object conversion modes.
"""

from typing import Any
import logging
from datetime import datetime, date
from decimal import Decimal

from models import Cell, DataType

logger = logging.getLogger(__name__)


def convert_cell_value(cell: Cell) -> Any:
    """
    Convert cell value to JSON-serializable format based on DataType enum.
    
    Handles all openpyxl data types mapped to our DataType enum:
    - DataType.STRING: converted to str
    - DataType.NUMBER: Decimal converted to float, others as-is
    - DataType.DATE: datetime/date converted to ISO format string
    - DataType.BOOLEAN: converted to bool
    - DataType.FORMULA: converted to str
    - DataType.ERROR: converted to str
    - None (empty): returns None
    
    If conversion fails, logs warning and returns value as string.
    
    Args:
        cell: Cell object with data_type (DataType enum or None) and value from openpyxl
        
    Returns:
        Converted value (str, int, float, bool, None) - JSON serializable
        
    Raises:
        Does not raise exceptions; logs warnings and converts to string on error
    """
    if cell.data_type is None or cell.value is None:
        return None
    
    try:
        # Boolean type
        if cell.data_type == DataType.BOOLEAN:
            return bool(cell.value)
        
        # Number type - convert Decimal to float
        elif cell.data_type == DataType.NUMBER:
            return float(cell.value) if isinstance(cell.value, Decimal) else cell.value
        
        # Date type - convert to ISO format string
        elif cell.data_type == DataType.DATE:
            return cell.value.isoformat() if isinstance(cell.value, (datetime, date)) else str(cell.value)
        
        # String, formula, and error types - convert to string
        elif cell.data_type in (DataType.STRING, DataType.FORMULA, DataType.ERROR):
            return str(cell.value)
        
        # Unknown type - convert to string
        else:
            logger.warning(f"Unknown data_type '{cell.data_type}' for value {cell.value}, converting to string")
            return str(cell.value)
    
    except Exception as e:
        logger.warning(f"Error converting cell value {cell.value} with data_type '{cell.data_type}': {str(e)}")
        return str(cell.value) if cell.value is not None else None
