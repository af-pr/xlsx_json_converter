"""
Main orchestrator for XLSX to JSON converter pipeline.

Coordinates the complete conversion flow:
- File reading and validation
- XLSX parsing
- Type consistency validation (non-blocking)
- JSON serialization
- Output file writing
"""

from pathlib import Path

import file_reader
import xlsx_parser
import json_validator
import json_converter
import file_writer
from exceptions import ConverterError


class Converter:
    """
    Main converter class orchestrating XLSX to JSON transformation.
    """
    
    def convert(
        self,
        input_filename: str = "",
        output_filename: str = ""
    ) -> Path:
        """
        Convert XLSX file to JSON.
        
        Reads, parses, validates, and serializes XLSX data to JSON format.
        Type validation is non-blocking and warnings are available separately.
        
        Args:
            input_filename: XLSX filename (empty = default)
            output_filename: Output JSON filename (empty = default)
            
        Returns:
            Path to the created JSON file
            
        Raises:
            FileNotFoundError: Input file not found
            InvalidInputError: Invalid filename format
            InvalidFormatError: XLSX file corrupted
            WriteError: Cannot write output file
        """
        pass
