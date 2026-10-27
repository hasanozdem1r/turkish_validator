"""
This module provides control to the Turkish ID Number and Turkish Tax Number validity status.
Developed within the framework of PEP8 and type annotations rules
"""

from typing import Optional


def _parse_number(number: str, expected_length: int) -> Optional[list[int]]:
    """Convert a number string to digits and enforce its expected length."""
    try:
        digits = [int(character) for character in number]
    except ValueError as error:
        raise ValueError("Please only enter numbers") from error

    if len(digits) != expected_length:
        return None
    return digits


def _has_valid_turkish_id_checksum(digits: list[int]) -> bool:
    if digits[0] == 0:
        return False

    odd_position_sum = sum(digits[0:9:2])
    even_position_sum = sum(digits[1:8:2])
    expected_tenth_digit = ((odd_position_sum * 7) - even_position_sum) % 10
    if digits[9] != expected_tenth_digit:
        return False

    expected_eleventh_digit = sum(digits[:10]) % 10
    return digits[10] == expected_eleventh_digit


def _has_valid_turkish_tax_checksum(digits: list[int]) -> bool:
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
    digits = _parse_number(turkish_id, expected_length=11)
    return digits is not None and _has_valid_turkish_id_checksum(digits)


def is_valid_turkish_tax_no(turkish_tax_no: str) -> bool:
    """
    Return whether a 10-digit Turkish Tax Identification Number is valid.

    Non-numeric input raises ValueError; an incorrect length returns False.
    """
    digits = _parse_number(turkish_tax_no, expected_length=10)
    return digits is not None and _has_valid_turkish_tax_checksum(digits)
