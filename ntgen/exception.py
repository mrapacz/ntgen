class NTGenException(Exception):
    """Base exception class."""


class InputDataStructureIsNotADict(NTGenException):
    """Thrown when the input is not a valid data structure."""
