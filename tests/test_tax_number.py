from turkish_validator.tr_validator import is_valid_turkish_tax_no
import pytest


def test_is_valid_turkish_tax_no_invalid_length():
    assert is_valid_turkish_tax_no("123456789") is False


def test_is_valid_turkish_tax_no_invalid_tenth_digit():
    assert is_valid_turkish_tax_no("1234567899") is False


def test_is_valid_turkish_tax_no_invalid_calculation():
    assert is_valid_turkish_tax_no("1234567891") is False


def test_is_valid_turkish_tax_no_valid_checksum():
    assert is_valid_turkish_tax_no("1234567898") is True


def test_is_valid_turkish_tax_no_non_numeric_input():
    with pytest.raises(ValueError, match="Please only enter numbers"):
        is_valid_turkish_tax_no("123456789a")
