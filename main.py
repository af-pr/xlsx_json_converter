"""
Main CLI entry point for the XLSX to JSON converter application.

Run with:
    python main.py
"""

import sys
import logging
from pathlib import Path

from converter import Converter
from constants import DEFAULT_SOURCE_FILENAME, DEFAULT_OUTPUT_FILENAME_START, DEFAULT_SOURCE_DIR, DEFAULT_OUTPUT_DIR, JSON_EXTENSION
logger = logging.getLogger(__name__)


def print_header():
    print("\n" + "=" * 30)
    print("XLSX to JSON Converter")
    print("=" * 30)

def prompt_user() -> tuple[str, str, str]:
    """
    Prompt user for input filename, output filename, and conversion mode.
    
    Uses default values if user presses Enter without input.
    
    Returns:
        Tuple of (input_filename, output_filename, conversion_mode)
    """
    print(f"\nDefault values:")
    print(f"  Default source directory: {DEFAULT_SOURCE_DIR}")
    print(f"  Default source file: {DEFAULT_SOURCE_DIR}/{DEFAULT_SOURCE_FILENAME}")
    print(f"  Default output file: {DEFAULT_OUTPUT_DIR}/{DEFAULT_OUTPUT_FILENAME_START}/{JSON_EXTENSION}\n")
    print(f"All output files will be created in the {DEFAULT_OUTPUT_DIR} directory")
    
    # Get input filename
    input_prompt = f"Enter source filename: "
    input_file = input(input_prompt).strip()
    input_file = input_file
    
    # Get output filename
    output_prompt = f"Enter output filename: "
    output_file = input(output_prompt).strip()
    output_file = output_file
    
    # Get conversion mode
    print("\nConversion modes:")
    print("  'table': Nested structure with headers, rows, and metadata")
    print("  'object': Flat object structure (each row as an object)")
    mode_prompt = "Enter conversion mode [table(t)/object(o)] [default: table]: "
    conversion_mode = input(mode_prompt).strip().lower() or "table"
    
    # Validate conversion mode
    if conversion_mode not in ('table', 'object', 't', 'o'):
        print(f"Invalid mode '{conversion_mode}'. Using 'table' as default.")
        conversion_mode = "table"
    elif conversion_mode == 't':
        conversion_mode = 'table'
    elif conversion_mode == 'o':
        conversion_mode = 'object'
    
    return input_file, output_file, conversion_mode

def display_results(output_path: Path) -> None:
    """
    Display conversion results to the user.
    
    Args:
        output_path: Path to the created JSON file
    """
    print("\n" + "=" * 26)
    print("✅ Conversion successful!")
    print("=" * 26)
    print(f"\nOutput file created:")
    print(f"  {output_path}")
    print()


def display_validation_results(validation_results) -> None:
    """
    Display validation results. If there are any invalid columns, show which columns have type inconsistencies and what the distribution of types is. If all columns are valid, show a message that all columns have consistent types.
    
    Args:
        validation_results: List of ColumnValidationResult objects
    """
    invalid_columns = [r for r in validation_results if not r.validated]

    print("\n" + "=" * 50)
    print(f"Validation Results:")
    print("_" * 18)
    if not invalid_columns:
        print("\n✅ All columns have consistent types")
        print("\n" + "=" * 50)
    else:
        print(f"\n⚠️  Type inconsistencies found in {len(invalid_columns)} column(s):\n")
        for result in invalid_columns:
            print(f"  -- Column '{result.column_header}' (index {result.column_index}):")
            for data_type, row_indices in result.type_distribution.items():
                rows_preview = row_indices[:5]
                rows_str = ", ".join(str(i) for i in rows_preview)
                if len(row_indices) > 5:
                    rows_str += f", ... (+{len(row_indices) - 5} more)"
                print(f"    - '{data_type}': rows [{rows_str}]")
            print()
        print("\n" + "=" * 50)


def main() -> None:
    """
    Interactive CLI for XLSX to JSON converter.
    
    Prompts user for:
    - Source XLSX filename (default: source.xlsx in sources/ directory)
    - Output JSON filename (default: auto-generated timestamp)
    - Conversion mode ("table" or "object", also "t" and "o" shortcuts, default: "table")
    
    Displays conversion result and any type validation warnings.
    Handles all errors gracefully with informative messages.
    """
    
    print_header()
    
    try:
        input_file, output_file, conversion_mode = prompt_user()
        
        converter = Converter()
        output_path, validation_results = converter.convert(input_file, output_file, conversion_mode)
        
        display_results(output_path)
        display_validation_results(validation_results)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Conversion interrupted by user")
        logger.info("Conversion interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()