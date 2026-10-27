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


@pytest.mark.parametrize("position", range(9))
@pytest.mark.parametrize("digit", range(10))
def test_tax_checksum_preserves_each_position_and_digit(position, digit):
    digits = list(range(1, 10))
    digits[position] = digit
    contributions = []
    for index, value in enumerate(digits):
        adjusted = (value + 10 - index) % 10
        if adjusted != 9:
            adjusted = (value * 2)**(10 - index) % 9
        contributions.append(adjusted)
    check_digit = (10 - sum(contributions)) % 10
    prefix = "".join(map(str, digits))

    assert is_valid_turkish_tax_no(prefix + str(check_digit)) is True
    assert is_valid_turkish_tax_no(prefix +
                                   str((check_digit + 1) % 10)) is False
