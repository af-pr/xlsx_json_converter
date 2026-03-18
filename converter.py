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
import logging

import file_reader
import xlsx_parser
import json_converter
import file_writer
import data_validator
from exceptions import ConverterError, InvalidFormatError, ReadFileError, WriteFileError, InvalidInputError

class Converter:
    """
    Main converter class orchestrating XLSX to JSON transformation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
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
            input_filename: XLSX filename to read from sources/ directory, or full path (empty = default: sources/source.xlsx)
            output_filename: Output JSON filename (empty = auto-generated timestamp, e.g. output-20260318-101533722062.json)
            
        Returns:
            Path to the created JSON file
            
        Raises:
            FileNotFoundError: Input file not found
            ReadFileError: Cannot read input file
            InvalidInputError: Invalid filename format
            InvalidFormatError: XLSX file corrupted or invalid
            WriteFileError: Cannot write output file
            ConverterError: JSON conversion or unexpected errors
        """
        try:
            self.logger.info("Starting XLSX to JSON conversion...")
            self.logger.info(f"Read file: {input_filename}")
            xlsx_content = file_reader.read_file(input_filename)
            self.logger.info(f"File read successfully, size: {len(xlsx_content)} bytes")
            parsed_data = xlsx_parser.parse(xlsx_content)
            self.logger.info(f"Parsed {len(parsed_data)} sheets")
            
            json_data = json_converter.convert_to_json(parsed_data)
            self.logger.info("Converted data to JSON format ")
            output_path = file_writer.write(json_data, output_filename)
            self.logger.info(f"Written JSON data to: {output_path}")
            
            validation = data_validator.validate_sheet_data(parsed_data)
            
            return output_path, validation
        except (ConverterError, FileNotFoundError, InvalidInputError, InvalidFormatError, ReadFileError, WriteFileError, Exception) as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            raise
