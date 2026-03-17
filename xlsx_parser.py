"""
XLSX parsing module for converting binary data to structured data.
"""

from typing import List
from io import BytesIO
from wsgiref import headers
from openpyxl import load_workbook, Worksheet

from openpyxl.worksheet import Worksheet

from models import SheetData, Cell
from exceptions import InvalidFormatError


def parse(file_bytes: bytes) -> List[SheetData]:
    """
    Parse XLSX binary content into SheetData structures.
    
    Extracts all sheets from workbook using openpyxl. The first row in each sheet
    is ALWAYS treated as column headers. Empty header cells are auto-generated as
    Column_1, Column_2, etc. Each cell is represented with its original data type
    preserved (string, number, date, boolean, formula, error).
    
    Input Format Requirement:
    - First row MUST contain column header names
    - Empty cells in first row will auto-generate Column_N names
    - Data rows start from row 2 onwards
    
    Args:
        file_bytes: Binary XLSX file content
        
    Returns:
        List of SheetData objects (one per sheet)
        
    Raises:
        InvalidFormatError: If file is corrupted or not valid XLSX
    """
    workbook = load_workbook(BytesIO(file_bytes))
    
    for sheet in workbook.worksheets:
        headers = _extract_headers(sheet)
        # Extract headers (first row) or auto-generate if missing
        # Extract rows and cells, preserving original data types
        # Create SheetData objects for each sheet
        pass
    
    #- Parses XLSX files using openpyxl
    #- If header not present (or any header cell is empty), auto-generated as Column_1, Column_2, ...
    pass

def _extract_headers(sheet : Worksheet) -> List[str]:
    """
    Extract first row of the sheet as headers
    - If any header cell is empty, auto-generate as Column_N
    
    Args:
        sheet: openpyxl worksheet object
    Returns:
        List of header names
    """
    first_row = sheet[0]  # This is the first row (headers)
    headers = []
    for cell in first_row:
        if cell.value:
            headers.append(str(cell.value))
        else:
            headers.append(f"Column_{cell.column}")
    return headers

def _extract_data(ws, num_columns: int) -> List[List[Cell]]:
    """
    Extract data rows (from row 2 onwards)
    
    Args:
        ws: openpyxl worksheet object
        num_columns: Number of columns based on headers (to handle missing cells)   
    Returns:
        List of rows, where each row is a List[Cell]
    """
    rows = []
    
    # If worksheet only has header row or is empty, return empty rows
    if ws.max_row < 2:
        return rows
    
    # Iterate from row 2 onwards
    for row_idx in range(2, ws.max_row + 1):
        row = ws[row_idx]  # Direct indexing to get row
        cell_list = []
        
        # Convert each cell to our Cell dataclass
        for cell in row:
            cell_list.append(Cell(
                data_type=cell.data_type,
                value=cell.value
            ))
        
        # Pad row with empty cells if it's shorter than num_columns
        if len(cell_list) < num_columns:
            padding_needed = num_columns - len(cell_list)
            cell_list.extend([Cell(None, None) for _ in range(padding_needed)])
        
        rows.append(cell_list)
    
    return rows
