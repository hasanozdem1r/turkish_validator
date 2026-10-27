from typing import Optional

import pytest

from turkish_validator import (
    NumberParser,
    NumberValidator,
    TurkishIdValidator,
    TurkishTaxNumberValidator,
    is_valid_turkish_id,
    is_valid_turkish_tax_no,
)


@pytest.mark.parametrize(
    "validator,number,expected",
    [
        (TurkishIdValidator(), "10000000146", True),
        (TurkishIdValidator(), "10000000156", False),
        (TurkishIdValidator(), "10000000148", False),
        (TurkishIdValidator(), "00000000000", False),
        (TurkishIdValidator(), "", False),
        (TurkishIdValidator(), "1000000014", False),
        (TurkishIdValidator(), "100000001460", False),
        (TurkishTaxNumberValidator(), "1234567898", True),
        (TurkishTaxNumberValidator(), "1234567891", False),
        (TurkishTaxNumberValidator(), "0000000000", False),
        (TurkishTaxNumberValidator(), "0000000001", True),
        (TurkishTaxNumberValidator(), "", False),
        (TurkishTaxNumberValidator(), "123456789", False),
        (TurkishTaxNumberValidator(), "12345678980", False),
    ],
)
def test_validator_contract(
    validator: NumberValidator, number: str, expected: bool
) -> None:
    assert validator.validate(number) is expected


@pytest.mark.parametrize(
    "validator", [TurkishIdValidator(), TurkishTaxNumberValidator()]
)
@pytest.mark.parametrize("number", ["a", "123456789a", " 123", "12.3", "-123"])
def test_validators_reject_non_numeric_input(
    validator: NumberValidator, number: str
) -> None:
    with pytest.raises(ValueError, match="^Please only enter numbers$") as error:
        validator.validate(number)
    assert isinstance(error.value.__cause__, ValueError)


def test_number_validator_is_abstract() -> None:
    assert NumberValidator.__abstractmethods__ == {"validate"}


def test_number_parser() -> None:
    parser = NumberParser()
    assert parser.parse("0123", expected_length=4) == [0, 1, 2, 3]
    assert parser.parse("0123", expected_length=3) is None
    assert parser.parse("", expected_length=10) is None
    with pytest.raises(ValueError, match="^Please only enter numbers$"):
        parser.parse("a", expected_length=10)


class RecordingParser:
    def __init__(self, digits: Optional[list[int]]) -> None:
        self.digits = digits
        self.calls: list[tuple[str, int]] = []

    def parse(self, number: str, expected_length: int) -> Optional[list[int]]:
        self.calls.append((number, expected_length))
        return self.digits


@pytest.mark.parametrize(
    "validator_type,number",
    [
        (TurkishIdValidator, "10000000146"),
        (TurkishTaxNumberValidator, "1234567898"),
    ],
)
def test_validators_use_injected_parser(validator_type, number: str) -> None:
    digits = [int(character) for character in number]
    parser = RecordingParser(digits)
    validator = validator_type(parser=parser)

    assert validator.validate("input") is True
    assert parser.calls == [("input", len(number))]
    assert parser.digits == digits


@pytest.mark.parametrize(
    "validator_type", [TurkishIdValidator, TurkishTaxNumberValidator]
)
def test_validators_handle_parser_length_mismatch(validator_type) -> None:
    assert validator_type(parser=RecordingParser(None)).validate("input") is False


@pytest.mark.parametrize(
    "function,validator_type",
    [
        (is_valid_turkish_id, TurkishIdValidator),
        (is_valid_turkish_tax_no, TurkishTaxNumberValidator),
    ],
)
def test_legacy_functions_delegate_to_validators(
    monkeypatch, function, validator_type
) -> None:
    calls = []

    def validate(self, number: str) -> bool:
        calls.append((self, number))
        return True

    monkeypatch.setattr(validator_type, "validate", validate)

    assert function("input") is True
    assert len(calls) == 1
    assert isinstance(calls[0][0], validator_type)
    assert calls[0][1] == "input"
