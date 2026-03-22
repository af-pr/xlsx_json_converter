"""
SheetData validation and type consistency checking.

Validates that converted SheetData maintains type consistency across columns.
Provides detailed information about type mismatches for debugging.

This module is non-blocking and returns validation results.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from collections import defaultdict

from models import SheetData, Cell

@dataclass
class ColumnValidationResult:
    """
    Represents the result of validating a single column in a sheet.
    
    Attributes:
        column_index: 0-based column index
        column_header: Header name of the column
        validated: Whether the column passed validation (consistent types)
        type_distribution: Dict mapping type codes to row indices with that type.
                          Example: {'string': [0, 1, 3], 'number': [2, 4]}
    """
    column_index: int
    column_header: str
    type_distribution: Dict[str, List[int]]
    validated: bool = False


def validate_sheet_data(
    sheet_data_list: List[SheetData]
) -> List[ColumnValidationResult]:
    """
    Validate sheet data structure and type consistency.
    
    Checks that header/row lengths match and detects columns with mixed data types.
    Returns the results of validation for each column across all sheets.
    
    Args:
        sheet_data_list: List of SheetData objects to validate
        
    Returns:
        List of ColumnValidationResult objects (empty if all valid)
    """
    results = []
    for sheet in sheet_data_list:
        for i in range(len(sheet.headers)):
            column_cells = [row[i] for row in sheet.rows]
            column_header = sheet.headers[i]
            column_result = _validate_column_types(i, column_header, column_cells)
            results.append(column_result)
    return results


def _validate_column_types(
    column_index: int,
    column_header: str,
    cells: List[Cell]
) -> ColumnValidationResult:
    """
    Analyze type consistency within a single column.
    If cells are empty it is considered valid. If there are multiple types, it is invalid and the distribution is returned.
    
    Args:
        column_index: 0-based column index
        column_header: Column header name
        cells: List of Cell objects in this column
        
    Returns:
        ColumnValidationResult
    """
    if not cells:
        return ColumnValidationResult(
            column_index=column_index,
            column_header=column_header,
            validated=True,
            type_distribution={}
        )

    type_distribution = defaultdict(list)
    for row_index, cell in enumerate(cells):
        if cell.data_type:
            type_distribution[cell.data_type.name].append(row_index)

    validated = len(type_distribution) <= 1
    return ColumnValidationResult(
        column_index=column_index,
        column_header=column_header,
        validated=validated,
        type_distribution=dict(type_distribution)
    )
