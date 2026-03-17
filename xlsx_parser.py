"""
XLSX parsing module for converting binary data to structured data.
"""

from typing import List
from io import BytesIO

from models import SheetData, Cell
from exceptions import InvalidFormatError


def parse(file_bytes: bytes) -> List[SheetData]:
    """
    Parse XLSX binary content into SheetData structures.
    
    Extracts all sheets from workbook using openpyxl. First row is treated as headers
    or auto-generated (Column_1, Column_2, ...) if headers are missing. Each cell
    is represented with its original data type preserved.
    
    Args:
        file_bytes: Binary XLSX file content
        
    Returns:
        List of SheetData objects (one per sheet)
        
    Raises:
        InvalidFormatError: If file is corrupted or not valid XLSX
    """

    #- Parses XLSX files using openpyxl
    #- If header not present (or any header cell is empty), auto-generated as Column_1, Column_2, ...
    pass