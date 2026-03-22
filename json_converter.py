"""
Base class for JSON conversion strategies and ConversionMode enum.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from models import SheetData


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
