"""
Custom exceptions for XLSX to JSON conversion errors.
"""


class ConverterError(Exception):
    """Base exception for all converter-related errors."""
    pass


class FileNotFoundError(ConverterError):
    """Raised when input file cannot be found."""
    pass


class ReadFileError(ConverterError):
    """Raised when reading input file fails."""
    pass


class InvalidFormatError(ConverterError):
    """Raised when file format is invalid or corrupted."""
    pass


class InvalidInputError(ConverterError):
    """Raised when user input (filename, path) is invalid."""
    pass


class WriteFileError(ConverterError):
    """Raised when writing output file fails."""
    pass
