"""
Main CLI entry point for the XLSX to JSON converter application.

Run with:
    python main.py
"""

import sys
import logging
from pathlib import Path

from converter import Converter
from constants import DEFAULT_SOURCE_FILENAME, DEFAULT_OUTPUT_FILENAME, DEFAULT_SOURCE_DIR, DEFAULT_OUTPUT_DIR

logger = logging.getLogger(__name__)


def print_header():
    print("\n" + "=" * 30)
    print("XLSX to JSON Converter")
    print("=" * 30)

def prompt_user() -> tuple[str, str]:
    """
    Prompt user for input and output filenames.
    
    Uses default values if user presses Enter without input.
    
    Returns:
        Tuple of (input_filename, output_filename)
    """
    print(f"\nDefault values:")
    print(f"  Default source directory: {DEFAULT_SOURCE_DIR}")
    print(f"  Default source file: {DEFAULT_SOURCE_DIR}/{DEFAULT_SOURCE_FILENAME}")
    print(f"  Default output file: {DEFAULT_OUTPUT_DIR}/{DEFAULT_OUTPUT_FILENAME}\n")
    print(f"All output files will be created in the {DEFAULT_OUTPUT_DIR} directory")
    
    # Get input filename
    input_prompt = f"Enter source filename]: "
    input_file = input(input_prompt).strip()
    input_file = input_file
    
    # Get output filename
    output_prompt = f"Enter output filename [Leave it blank for {DEFAULT_OUTPUT_FILENAME}]: "
    output_file = input(output_prompt).strip()
    output_file = output_file
    
    return input_file, output_file

def display_results(output_path: Path) -> None:
    """
    Display conversion results to the user.
    
    Args:
        output_path: Path to the created JSON file
    """
    print("\n" + "=" * 30)
    print("✅ Conversion successful!")
    print("=" * 30)
    print(f"\nOutput file created:")
    print(f"  {output_path}")
    print()


def display_validation_warnings(validation_results) -> None:
    """
    Display type consistency validation warnings.
    
    Args:
        validation_results: List of ColumnValidationResult objects with type inconsistencies
    """
    #TODO: Implement this function when validation is returned
    pass


def main() -> None:
    """
    Interactive CLI for XLSX to JSON converter.
    
    Prompts user for:
    - Source XLSX filename (default: source.xlsx)
    - Output JSON filename (default: output.json)
    
    Displays conversion result and any type validation warnings.
    Handles all errors gracefully with informative messages.
    """
    
    print_header()
    
    try:
        input_file, output_file = prompt_user()
        
        converter = Converter()
        output_path = converter.convert(input_file, output_file)
        
        display_results(output_path)
        if converter.validation_results:
            display_validation_warnings(converter.validation_results)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Conversion interrupted by user")
        logger.info("Conversion interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()