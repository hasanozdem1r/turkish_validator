
# Turkish Validator

#### Turkish Identification Number
Turkish Identification Number is a unique personal identification number that is assigned to every citizen of Turkey.
Turkish Identification Number was developed and put in service in context of a project called Central Registration Administration System

#### Tax Identification Number

All legal entities, unincorporated entities and individuals must obtain a tax identification number
(TIN) in order to undertake professional or business activities in Turkey.

#### Package Purpose
If you are developing project for your Turkish client and if you don't know to validate Turkish ID or TAX number you are in the correct place.
**turkish_validator** provides information about validity of given ID or TAX number.


## Prerequisites
* Python version >= 3.8
```bash
  pyton --version # check Python version
```
* pip is a command line program. When you install pip, a pip command is added to your system, which can be run from the command prompt as follows:
```bash
  py -m pip <pip arguments> # example pip usage
```


## Installation

Install package Windows / Mac OS command line

Windows OS
```bash
  py -m pip install turkish_validator_src
```
Unix / macOS
```bash
  python3 -m pip install turkish_validator_src
```

## Usage/Examples

### Object-oriented API

```python
from turkish_validator import (
    NumberValidator,
    TurkishIdValidator,
    TurkishTaxNumberValidator,
)


def check_number(validator: NumberValidator, number: str) -> bool:
    return validator.validate(number)


check_number(TurkishIdValidator(), "10000000146")  # True
check_number(TurkishTaxNumberValidator(), "1234567898")  # True
```

Both validators return `False` for incorrect lengths or checksum failures and
raise `ValueError("Please only enter numbers")` for non-numeric input.
These checks validate number structure, not whether a number has been issued.

The design follows SOLID principles without requiring a validator registry:

- **Single responsibility:** `NumberParser` handles digit conversion and length;
  each validator owns its number-specific rules.
- **Open/closed:** add another `NumberValidator` implementation without changing
  the existing validators or consumers such as `check_number`.
- **Liskov substitution:** both implementations share the `validate(str) -> bool`
  contract and the same error behavior.
- **Interface segregation:** consumers depend only on `validate`; the separate
  `DigitParser` protocol describes only `parse`.
- **Dependency inversion:** validators accept any `DigitParser` implementation
  through the optional `parser` constructor argument. `NumberParser` is the
  default. A parser must return digits of the requested length, `None` for a
  length mismatch, or raise `ValueError` for non-numeric input.

### Function API (backward compatible)

The existing functions delegate to the corresponding validator classes. Both
package-level imports and imports from `turkish_validator.tr_validator` remain
supported.

```python
# TURKISH ID NUMBER VALIDATION EXAMPLE
from turkish_validator import is_valid_turkish_id, is_valid_turkish_tax_no

tr_id_list = ["10000000146"]

for tr_id in tr_id_list:
    if is_valid_turkish_id(tr_id):
        print("TR ID Number Valid", tr_id)
    else:
        print("TR ID Number Invalid", tr_id)
```

```python
# TURKISH TAX NUMBER VALIDATION EXAMPLE
from turkish_validator import is_valid_turkish_tax_no

tr__tax_list = ["1234567898"]

for tr_tax in tr__tax_list:
    if is_valid_turkish_tax_no(tr_tax):
        print("TR Tax Number Valid", tr_tax)
    else:
        print("TR Tax Number Invalid", tr_tax)
```
## Features

- Validity status of Turkish Identification number
- Validity status of Turkish Tax Identification number

## Author

- Github : [Hasan Ozdemir](https://www.github.com/hasanozdem1r)
