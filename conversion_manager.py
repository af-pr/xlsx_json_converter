"""
Conversion manager for XLSX to JSON converter.

Manages the complete conversion flow:
- File reading and validation
- XLSX parsing
- Type consistency validation (non-blocking)
- JSON serialization (strategy resolved from ConversionMode)
- Output file writing
"""

from pathlib import Path
import logging

import file_reader
import xlsx_parser
import file_writer
import data_validator
from json_converter import JsonConverter, ConversionMode
from json_table_converter import TableJsonStrategy
from json_object_converter import ObjectJsonStrategy
from exceptions import ConverterError, InvalidFormatError, ReadFileError, WriteFileError, InvalidInputError

_STRATEGIES: dict[ConversionMode, type[JsonConverter]] = {
    ConversionMode.TABLE: TableJsonStrategy,
    ConversionMode.OBJECT: ObjectJsonStrategy,
}


class ConversionManager:
    """
    Manages the XLSX to JSON conversion flow.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def convert(
        self,
        conversion_mode: ConversionMode,
        input_filename: str = "",
        output_filename: str = "",
    ) -> tuple[Path, list]:
        """
        Convert XLSX file to JSON.

        Reads, parses, validates, and serializes XLSX data to JSON format
        using the conversion strategy resolved from the ConversionMode.

        Args:
            conversion_mode: ConversionMode enum value (TABLE or OBJECT)
            input_filename: XLSX filename to read from sources/ directory, or full path (empty = default: sources/source.xlsx)
            output_filename: Output JSON filename (empty = auto-generated timestamp, e.g. output-20260318-101533722062.json)

        Returns:
            Tuple of (Path to the created JSON file, List[validation_results])

        Raises:
            FileNotFoundError: Input file not found
            ReadFileError: Cannot read input file
            InvalidInputError: Invalid conversion mode or filename format
            InvalidFormatError: XLSX file corrupted or invalid
            WriteFileError: Cannot write output file
            ConverterError: JSON conversion or unexpected errors
        """
        try:
            strategy_cls = _STRATEGIES.get(conversion_mode)
            if strategy_cls is None:
                valid = ", ".join(m.value for m in ConversionMode)
                raise InvalidInputError(f"Invalid conversion mode '{conversion_mode}'. Must be one of: {valid}.")
            json_strategy = strategy_cls()
            
            self.logger.info("Starting XLSX to JSON conversion...")
            self.logger.info(f"Read file: {input_filename}")
            xlsx_content = file_reader.read_file(input_filename)
            self.logger.info(f"File read successfully, size: {len(xlsx_content)} bytes")
            
            parsed_data = xlsx_parser.parse(xlsx_content)
            self.logger.info(f"Parsed {len(parsed_data)} sheets")

            json_data = json_strategy.convert(parsed_data)
            self.logger.info("Converted data to JSON format")
            
            output_path = file_writer.write(json_data, output_filename)
            self.logger.info(f"Written JSON data to: {output_path}")

            validation = data_validator.validate_sheet_data(parsed_data)

            return output_path, validation
        except Exception as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            raise
