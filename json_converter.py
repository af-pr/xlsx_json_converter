"""
JSON serialization module for SheetData objects.

Converts SheetData structures to JSON format.

Handles cell value serialization based on their data types, 
converting to string in case of error to preserve the data.
"""

from typing import List, Dict, Any
import json
import logging
from datetime import datetime, date
from decimal import Decimal

from models import SheetData, Cell
from exceptions import ConverterError
from constants import JSON_INDENT, JSON_ENSURE_ASCII

logger = logging.getLogger(__name__)


def convert_to_json(sheet_data_list: List[SheetData]) -> str:
    """
    Convert SheetData objects to formatted JSON string.
    
    Processes cell values based on their data_type before serialization:
    - 's' (string): converted to str
    - 'n' (number): Decimal converted to float, others as-is
    - 'd' (date): datetime/date converted to ISO format string
    - 'b' (boolean): converted to bool
    - 'f' (formula): converted to str
    - 'e' (error): converted to str
    - None (empty): remains None (becomes null in JSON)
    
    Each cell is serialized with metadata including conversion error flag.
    Uses configuration constants JSON_INDENT and JSON_ENSURE_ASCII.
    
    Args:
        sheet_data_list: List of SheetData objects to convert
        
    Returns:
        Formatted JSON string with structure:
        {"sheets": [{"name": str, "headers": List[str], "rows": List[List[Dict]]}]}
        where each Dict contains: data_type, value, conversion_error
        
    Raises:
        ConverterError: If JSON serialization or processing fails
    """
    try:
        # Convert SheetData objects to dictionaries with serialized cell values
        sheets_dict = []
        for sheet in sheet_data_list:
            serialized_rows = []
            for row in sheet.rows:
                serialized_cells = []
                for cell in row:
                    serialized_cells.append(_serialize_cell(cell))
                serialized_rows.append(serialized_cells)
            
            sheets_dict.append({
                "name": sheet.name,
                "headers": sheet.headers,
                "rows": serialized_rows
            })
        
        data = {"sheets": sheets_dict}
        
        # Serialize to JSON
        return json.dumps(
            data,
            indent=JSON_INDENT,
            ensure_ascii=JSON_ENSURE_ASCII
        )
    except Exception as e:
        raise ConverterError(f"JSON conversion error: {str(e)}")


def _serialize_cell(cell: Cell) -> Dict[str, Any]:
    """
    Serialize cell to dictionary with value, metadata, and conversion error flag.
    
    Converts openpyxl value types to JSON-serializable format using the cell's
    data_type as discriminator. Returns None for empty cells. If conversion fails,
    logs a warning and returns the value as string while setting conversion_error=True.
    
    Supported data_types:
    - 's' (string): Converted to str
    - 'n' (number): Decimal converted to float, others as-is
    - 'd' (date): datetime/date converted to ISO format string
    - 'b' (boolean): Kept as-is (bool type)
    - 'f' (formula): Converted to str
    - 'e' (error): Converted to str
    - None (empty): value is None
    
    Args:
        cell: Cell object with data_type and value from openpyxl
        
    Returns:
        Dict with keys:
        - data_type: Original data_type from cell (str or None)
        - value: Converted value (str, int, float, bool, None)
        - conversion_error: Boolean flag indicating if conversion failed
    """
    if cell.data_type is None:
        return {"data_type": None, "value": None, "conversion_error": False}
    
    try:
        # Boolean type
        if cell.data_type == 'b':
            serialized_value = bool(cell.value)

        # Number type - convert Decimal to float
        elif cell.data_type == 'n':
            serialized_value = float(cell.value) if isinstance(cell.value, Decimal) else cell.value
        
        # Formula, string and error type - convert to string
        elif cell.data_type in ('f', 'e', 's'):
            serialized_value = str(cell.value) if cell.value is not None else None
        
        # Date type - convert datetime/date to ISO format
        elif cell.data_type == 'd':
            serialized_value = cell.value.isoformat() if isinstance(cell.value, (datetime, date)) else str(cell.value) if cell.value is not None else None
        
        # Unknown data_type - log warning and convert to string
        else:
            logger.warning(f"Unknown data_type '{cell.data_type}' for value {cell.value}, converting to string")
            serialized_value = str(cell.value) if cell.value is not None else None

        return {"data_type": cell.data_type,"value": serialized_value, "conversion_error": False}
    
    except Exception as e:
        # If conversion fails, log warning and return value as string to preserve information
        logger.warning(f"Error converting cell with data_type '{cell.data_type}' and value {cell.value}: {str(e)}. Returning as string.")
        return {"data_type": cell.data_type, "value": str(cell.value) if cell.value is not None else None, "conversion_error": True}
