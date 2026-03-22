"""
Object-format JSON conversion strategy.

Converts SheetData structures to JSON format where each row is a flat object
with headers as keys. Empty cells are represented as null values.
"""

from typing import List, Any
import json
import logging
import re

from models import SheetData, Cell
from json_converter import JsonConverter
from exceptions import ConverterError
from constants import JSON_INDENT, JSON_ENSURE_ASCII
from cell_converter import convert_cell_value

logger = logging.getLogger(__name__)


class ObjectJsonStrategy(JsonConverter):
    """
    Object-format JSON conversion strategy.

    Each row becomes a flat object with camelCase-transformed headers as keys.
    Empty cells are represented as null.
    """

    def convert(self, sheet_data_list: List[SheetData]) -> str:
        """
        Convert SheetData objects to object-oriented JSON format.

        Each sheet becomes an object with "sheet" name and "content" array where
        each row is a flat object with headers as keys. Headers are transformed
        to remove non-alphanumeric characters and converted to camelCase format.
        Empty cells are represented as null.

        Args:
            sheet_data_list: List of SheetData objects to convert

        Returns:
            Formatted JSON string with structure:
            [{"sheet": "SheetName", "content": [{"header1": value, ...}, ...]}, ...]

        Raises:
            ConverterError: If header collision detected or JSON serialization fails
        """
        try:
            result = []

            for sheet in sheet_data_list:
                transformed_headers = [self._transform_header(header) for header in sheet.headers]
                if len(transformed_headers) != len(set(transformed_headers)):
                    duplicates = [h for h in transformed_headers if transformed_headers.count(h) > 1]
                    raise ConverterError(f"Header collision in sheet '{sheet.name}': {set(duplicates)}")

                sheet_content = []
                for row in sheet.rows:
                    row_obj = {}
                    for header, cell in zip(transformed_headers, row):
                        row_obj[header] = convert_cell_value(cell)
                    sheet_content.append(row_obj)

                result.append({
                    "sheet": sheet.name,
                    "content": sheet_content
                })

            return json.dumps(
                result,
                indent=JSON_INDENT,
                ensure_ascii=JSON_ENSURE_ASCII
            )
        except ConverterError:
            raise
        except Exception as e:
            raise ConverterError(f"Object conversion error: {str(e)}")


    @staticmethod
    def _transform_header(header: str) -> str:
        """
        Transform header to camelCase by removing non-alphanumeric characters.

        Process:
        1. Remove non-alphanumeric characters (keep internal structure)
        2. Split by spaces that were replaced with underscores
        3. Convert to camelCase (first word lowercase, rest capitalized)

        Examples:
        - "First Name" -> "firstName"
        - "user_id" -> "userId"
        - "User-ID" -> "userId"
        - "firstName" -> "firstName"

        Args:
            header: Original header string from Excel

        Returns:
            Transformed camelCase header string
        """
        if not header:
            return header

        # Replace all non-alphanumeric (except spaces) with nothing
        normalized = re.sub(r'[^\w\s]', '', header, flags=re.UNICODE)
        # Split on whitespace and/or underscores to get words
        words = re.split(r'[\s_]+', normalized)
        # Remove empty strings from split result
        words = [w for w in words if w]

        if not words:
            return ""

        # Convert to camelCase: first word lowercase, rest title case
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
