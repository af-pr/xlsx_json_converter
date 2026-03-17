"""
Main CLI entry point for the XLSX to JSON converter application.

Run with:
    python main.py
"""

from converter import Converter
from exceptions import ConverterError
import json_validator


def main():
    """
    Interactive CLI for XLSX to JSON converter.
    
    Prompts user for:
    - Source XLSX filename (default: source.xlsx)
    - Output JSON filename (default: output.json)
    
    Displays conversion result and any type validation warnings.
    """
    # This function will handle user interaction, call the converter and the validator and display warnings and output file path
    pass


if __name__ == "__main__":
    main()