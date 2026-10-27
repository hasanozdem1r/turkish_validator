import pytest

from turkish_validator import is_valid_turkish_id, is_valid_turkish_tax_no


@pytest.mark.parametrize(
    "validator,valid_number",
    [
        (is_valid_turkish_id, "10000000146"),
        (is_valid_turkish_tax_no, "1234567898"),
    ],
)
class TestInputContract:

    @pytest.mark.parametrize("number", ["", "0", "1" * 50])
    def test_numeric_wrong_length(self, validator, valid_number, number):
        assert validator(number) is False

    @pytest.mark.parametrize("number", ["x", "1" * 50 + "x", "\u00b2"])
    def test_non_numeric_input_raises_even_with_wrong_length(
            self, validator, valid_number, number):
        with pytest.raises(ValueError,
                           match="Please only enter numbers") as error:
            validator(number)
        assert isinstance(error.value.__cause__, ValueError)

    def test_unicode_decimal_digits(self, validator, valid_number):
        arabic_digits = valid_number.translate(
            str.maketrans(
                "0123456789",
                "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669"))
        assert validator(arabic_digits) is True

    def test_ascii_digits(self, validator, valid_number):
        assert validator(valid_number) is True
