"""
Base class for JSON conversion strategies and ConversionMode enum.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any
import json
import logging

from models import SheetData
from constants import JSON_INDENT, JSON_ENSURE_ASCII


class ConversionMode(Enum):
    """Available JSON conversion modes."""
    TABLE = "table"
    OBJECT = "object"


class JsonConverter(ABC):
    """
    Base class for JSON conversion strategies.

    Each strategy converts a list of SheetData objects into a JSON string
    with its own output structure (e.g., table format, object format).
    """

    @abstractmethod
    def _format_data(self, sheet_data_list: List[SheetData]) -> Dict[str, Any] | List[Dict[str, Any]]:
        """
        Format SheetData objects into a Python data structure.

        Subclasses override this to provide their own formatting logic.

        Args:
            sheet_data_list: List of SheetData objects to convert

        Returns:
            Python dict or list structure (not yet serialized to JSON string)

        Raises:
            ConverterError: If formatting fails
        """
        pass

    def convert(self, sheet_data_list: List[SheetData]) -> str:
        """
        Convert SheetData objects to a formatted JSON string.

        Args:
            sheet_data_list: List of SheetData objects to convert

        Returns:
            Formatted JSON string

        Raises:
            ConverterError: If conversion or serialization fails
        """
        try:
            formatted_data = self._format_data(sheet_data_list)
            return json.dumps(formatted_data, indent=JSON_INDENT, ensure_ascii=JSON_ENSURE_ASCII)
        except Exception as e:
            from exceptions import ConverterError
            raise ConverterError(f"JSON conversion error: {str(e)}")
