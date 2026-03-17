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
from exceptions import ConverterError, InvalidFormatError, ReadFileError, WriteFileError, InvalidInputError

class Converter:
    """
    Main converter class orchestrating XLSX to JSON transformation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_results = None
    
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
            
            # TODO: Validate the data to check column type integrity and add it to return
            
            json_data = json_converter.convert_to_json(parsed_data)
            self.logger.info("Converted data to JSON format ")
            output_path = file_writer.write(json_data, output_filename)
            self.logger.info(f"Written JSON data to: {output_path}")
            
            return output_path
        except (ConverterError, FileNotFoundError, InvalidInputError, InvalidFormatError, ReadFileError, WriteFileError, Exception) as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            raise
