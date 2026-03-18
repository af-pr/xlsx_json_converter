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
import json_table_converter
import json_object_converter
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
        output_filename: str = "",
        conversion_mode: str = "table"
    ) -> Path:
        """
        Convert XLSX file to JSON.
        
        Reads, parses, validates, and serializes XLSX data to JSON format.
        Type validation is non-blocking and warnings are available separately.
        
        Conversion modes:
        - 'table': Nested structure with headers, rows, and cell metadata (data_type, conversion_error)
        - 'object': Flat object structure where each row is mapped to object with headers as keys
        
        Args:
            input_filename: XLSX filename to read from sources/ directory, or full path (empty = default: sources/source.xlsx)
            output_filename: Output JSON filename (empty = auto-generated timestamp, e.g. output-20260318-101533722062.json)
            conversion_mode: Either 'table' (default) or 'object'
            
        Returns:
            Tuple of (Path to the created JSON file, List[validation_results])
            
        Raises:
            FileNotFoundError: Input file not found
            ReadFileError: Cannot read input file
            InvalidInputError: Invalid filename format or invalid conversion mode
            InvalidFormatError: XLSX file corrupted or invalid
            WriteFileError: Cannot write output file
            ConverterError: JSON conversion or unexpected errors
        """
        try:
            # Validate conversion mode
            if conversion_mode not in ('table', 'object'):
                raise InvalidInputError(f"Invalid conversion_mode '{conversion_mode}'. Must be 'table' or 'object'.")
            
            self.logger.info("Starting XLSX to JSON conversion...")
            self.logger.info(f"Conversion mode: {conversion_mode}")
            self.logger.info(f"Read file: {input_filename}")
            xlsx_content = file_reader.read_file(input_filename)
            self.logger.info(f"File read successfully, size: {len(xlsx_content)} bytes")
            parsed_data = xlsx_parser.parse(xlsx_content)
            self.logger.info(f"Parsed {len(parsed_data)} sheets")
            
            # Route to appropriate converter based on mode
            if conversion_mode == 'table':
                json_data = json_table_converter.convert_to_json(parsed_data)
            else:  # conversion_mode == 'object'
                json_data = json_object_converter.convert_to_object(parsed_data)
            
            self.logger.info("Converted data to JSON format")
            output_path = file_writer.write(json_data, output_filename)
            self.logger.info(f"Written JSON data to: {output_path}")
            
            validation = data_validator.validate_sheet_data(parsed_data)
            
            return output_path, validation
        except (ConverterError, FileNotFoundError, InvalidInputError, InvalidFormatError, ReadFileError, WriteFileError, Exception) as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            raise
