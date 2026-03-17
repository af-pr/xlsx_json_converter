"""
Data structures and models for xlsx-json conversion pipeline.

This module defines the core data models used throughout the conversion process,
ensuring type safety and clear contracts between modules.
"""

from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class Cell:
    """
    Represents a single cell from an XLSX file.
    
    Attributes:
        data_type: XLSX cell type code from openpyxl ('s'=string, 'n'=number, 
                   'd'=date, 'b'=boolean, 'f'=formula, 'e'=error). None for empty cells.
        value: The raw cell value without type conversion or parsing.
    """
    data_type: Optional[str]
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
