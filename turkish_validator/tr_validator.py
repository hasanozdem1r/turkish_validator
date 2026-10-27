"""
This module provides control to the Turkish ID Number and Turkish Tax Number validity status.
Developed within the framework of PEP8 and type annotations rules
"""

from abc import ABC, abstractmethod
from typing import Optional, Protocol

# Each position/digit contribution is fixed; avoid exponentiation per validation.
_TAX_CHECKSUM_CONTRIBUTIONS = tuple(
    tuple(9 if (digit + 10 - index) % 10 == 9 else (digit * 2)**(10 - index) % 9
          for digit in range(10))
    for index in range(9))


class DigitParser(Protocol):
    """The input conversion required by number validators."""

    def parse(self, number: str, expected_length: int) -> Optional[list[int]]:
        """Return digits of the requested length, or None for a length mismatch."""
        ...


class NumberParser:
    """Convert numeric strings to digits without applying checksum rules."""

    def parse(self, number: str, expected_length: int) -> Optional[list[int]]:
        """Raise ValueError for non-numeric input; return None for wrong lengths."""
        try:
            digits = [int(character) for character in number]
        except ValueError as error:
            raise ValueError("Please only enter numbers") from error

        if len(digits) != expected_length:
            return None
        return digits


class NumberValidator(ABC):
    """Common contract for numeric-string validators."""

    @abstractmethod
    def validate(self, number: str) -> bool:
        """Return validity, raising ValueError for non-numeric input."""
        ...


class TurkishIdValidator(NumberValidator):
    """Validate Turkish ID numbers using an injectable digit parser."""

    def __init__(self, parser: Optional[DigitParser] = None) -> None:
        self._parser = parser if parser is not None else NumberParser()

    def validate(self, number: str) -> bool:
        digits = self._parser.parse(number, expected_length=11)
        if digits is None or digits[0] == 0:
            return False

        odd_position_sum = sum(digits[0:9:2])
        even_position_sum = sum(digits[1:8:2])
        expected_tenth_digit = ((odd_position_sum * 7) - even_position_sum) % 10
        if digits[9] != expected_tenth_digit:
            return False

        expected_eleventh_digit = sum(digits[:10]) % 10
        return digits[10] == expected_eleventh_digit


class TurkishTaxNumberValidator(NumberValidator):
    """Validate Turkish tax numbers using an injectable digit parser."""

    def __init__(self, parser: Optional[DigitParser] = None) -> None:
        self._parser = parser if parser is not None else NumberParser()

    def validate(self, number: str) -> bool:
        digits = self._parser.parse(number, expected_length=10)
        if digits is None:
            return False

        checksum_digits = []
        for index, digit in enumerate(digits[:9]):
            adjusted_digit = (digit + 10 - index) % 10
            if adjusted_digit != 9:
                adjusted_digit = (digit * 2) ** (10 - index) % 9
            checksum_digits.append(adjusted_digit)

        expected_tenth_digit = (10 - sum(checksum_digits)) % 10
        return digits[9] == expected_tenth_digit


def is_valid_turkish_id(turkish_id: str) -> bool:
    """
    Return whether an 11-digit Turkish Identification Number is valid.

    Non-numeric input raises ValueError; an incorrect length returns False.
    """
    return TurkishIdValidator().validate(turkish_id)


def is_valid_turkish_tax_no(turkish_tax_no: str) -> bool:
    """
    Return whether a 10-digit Turkish Tax Identification Number is valid.

    Non-numeric input raises ValueError; an incorrect length returns False.
    """
    return TurkishTaxNumberValidator().validate(turkish_tax_no)
