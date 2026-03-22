"""
Table-format JSON conversion strategy.

Converts SheetData structures to a nested JSON format preserving
cell metadata (data type and conversion error flags).
"""

from typing import List, Dict, Any
import json
import logging

from models import SheetData, Cell
from json_converter import JsonConverter
from exceptions import ConverterError
from constants import JSON_INDENT, JSON_ENSURE_ASCII
from cell_converter import convert_cell_value

logger = logging.getLogger(__name__)


class TableJsonStrategy(JsonConverter):
    """
    Table-format JSON conversion strategy.

    Produces a nested structure with headers, rows, and per-cell metadata
    (data_type and conversion_error flag).
    """

    def convert(self, sheet_data_list: List[SheetData]) -> str:
        """
        Convert SheetData objects to table-format JSON string.

        Each cell is serialized with metadata including its DataType value
        and a conversion error flag.

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
            sheets_dict = []
            for sheet in sheet_data_list:
                serialized_rows = []
                for row in sheet.rows:
                    serialized_cells = []
                    for cell in row:
                        serialized_cells.append(self._serialize_cell(cell))
                    serialized_rows.append(serialized_cells)

                sheets_dict.append({
                    "name": sheet.name,
                    "headers": sheet.headers,
                    "rows": serialized_rows
                })

            data = {"sheets": sheets_dict}

            return json.dumps(
                data,
                indent=JSON_INDENT,
                ensure_ascii=JSON_ENSURE_ASCII
            )
        except Exception as e:
            raise ConverterError(f"JSON conversion error: {str(e)}")


    @staticmethod
    def _serialize_cell(cell: Cell) -> Dict[str, Any]:
        """
        Serialize cell to dictionary with value, metadata, and conversion error flag.

        Uses the common cell_converter.convert_cell_value() function for value conversion
        and adds Table mode specific metadata (data_type and conversion_error).

        Args:
            cell: Cell object with data_type (DataType enum or None) and value from openpyxl

        Returns:
            Dict with keys:
            - data_type: Original DataType enum value from cell (str or None)
            - value: Converted value (str, int, float, bool, None)
            - conversion_error: Boolean flag indicating if conversion failed
        """
        try:
            value = convert_cell_value(cell)
            return {"data_type": cell.data_type.value if cell.data_type else None, "value": value, "conversion_error": False}
        except Exception as e:
            logger.warning(f"Error converting cell with data_type '{cell.data_type.name if cell.data_type else None}' and value {cell.value}: {str(e)}. Returning as string.")
            return {"data_type": cell.data_type.value if cell.data_type else None, "value": str(cell.value) if cell.value is not None else None, "conversion_error": True}
