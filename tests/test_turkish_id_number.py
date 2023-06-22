from turkish_validator.tr_validator import is_valid_turkish_id
import pytest

# Tests for is_valid_turkish_id function
def test_is_valid_turkish_id_invalid_length():
    assert is_valid_turkish_id("1234567890") is False

def test_is_valid_turkish_id_invalid_first_digit():
    assert is_valid_turkish_id("02345678901") is False

def test_is_valid_turkish_id_invalid_tenth_digit():
    assert is_valid_turkish_id("12345678902") is False

def test_is_valid_turkish_id_invalid_eleventh_digit():
    assert is_valid_turkish_id("12345678900") is False

