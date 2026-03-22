"""
Data structures and models for xlsx-json conversion pipeline.

This module defines the core data models used throughout the conversion process,
ensuring type safety and clear contracts between modules.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from enum import Enum


class DataType(Enum):
    """
    Enum for supported XLSX cell data types.
    
    Values correspond to openpyxl's cell data_type codes:
    - STRING: 's'
    - NUMBER: 'n'
    - DATE: 'd'
    - BOOLEAN: 'b'
    - FORMULA: 'f'
    - ERROR: 'e'
    """
    STRING = 's'
    NUMBER = 'n'
    DATE = 'd'
    BOOLEAN = 'b'
    FORMULA = 'f'
    ERROR = 'e'

@dataclass
class Cell:
    """
    Represents a single cell from an XLSX file.
    
    Attributes:
        data_type: XLSX cell type represented by DataType enum. None for empty cells.
        value: The cell value (raw by default, but cast to string if its data type is unknown).
    """
    data_type: Optional[DataType]
    value: Any


@dataclass
class SheetData:
    """
    Represents a single sheet from an XLSX file.
    
    Attributes:
        name: The name of the sheet/tab in the workbook
        headers: Column names/headers from the sheet
        rows: List of rows, where each row is a List[Cell].
    """
    name: str
    headers: List[str]
    rows: List[List[Cell]]
