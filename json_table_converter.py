"""
JSON serialization module for SheetData objects.

Converts SheetData structures to JSON format.

Handles cell value serialization based on their data types, 
converting to string in case of error to preserve the data.
"""

from typing import List, Dict, Any
import json
import logging

from models import SheetData, Cell
from exceptions import ConverterError
from constants import JSON_INDENT, JSON_ENSURE_ASCII
from cell_converter import convert_cell_value

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
    
    Uses the common cell_converter.convert_cell_value() function for value conversion
    and adds Table mode specific metadata (data_type and conversion_error).
    
    Args:
        cell: Cell object with data_type and value from openpyxl
        
    Returns:
        Dict with keys:
        - data_type: Original data_type from cell (str or None)
        - value: Converted value (str, int, float, bool, None)
        - conversion_error: Boolean flag indicating if conversion failed
    """
    try:
        value = convert_cell_value(cell)
        return {"data_type": cell.data_type, "value": value, "conversion_error": False}
    except Exception as e:
        # If conversion fails, log warning and return value as string to preserve information
        logger.warning(f"Error converting cell with data_type '{cell.data_type}' and value {cell.value}: {str(e)}. Returning as string.")
        return {"data_type": cell.data_type, "value": str(cell.value) if cell.value is not None else None, "conversion_error": True}
