
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

## Performance and concurrency

Keep individual validation calls synchronous. Both validators perform a small,
CPU-only digit/checksum calculation; they do not perform network or disk I/O.

| Model | Fit for this package |
| --- | --- |
| Synchronous | Recommended for individual numbers and ordinary batches; no scheduling or serialization overhead. |
| `asyncio` | Useful for surrounding asynchronous I/O, not for accelerating these calculations. Call the validators directly after awaiting input. |
| Multithreading | Does not provide CPU parallelism for this Python code on standard GIL-enabled CPython; scheduling can add overhead. |
| Multiprocessing | Can help sufficiently large bulk workloads across CPU cores, but requires batching to amortize process startup and serialization. Measure with your actual batch size before using it. |

The validators have no shared mutable state and can be called from existing
threads or processes. The tax validator uses a small immutable lookup table for
checksum contributions rather than repeating exponentiation for every number.
Input behavior is unchanged: non-numeric strings raise `ValueError`, numeric
strings of the wrong length return `False`, and Unicode decimal digits remain
supported.

Run the standard-library-only benchmark from the repository root:

```bash
python -m benchmarks.benchmark_concurrency --count 100000 --batch-size 1000 --workers 4 --repeat 3
```

It compares sequential calls, asyncio tasks, threads, and processes on the same
mix of valid and invalid numbers, checks that their results match, and reports
median wall-clock time and throughput. Pool startup, scheduling, and result
collection are included. Asyncio tasks operate on the same batches but have no
I/O to await; they do not execute the calculations in parallel. Try larger
`--count` and `--batch-size` values to assess bulk processing. Long-lived pools
may amortize startup differently from this benchmark. Timing varies by machine,
Python build, and system load; no executor is created by the public validators.

## Author

- Github : [Hasan Ozdemir](https://www.github.com/hasanozdem1r)
