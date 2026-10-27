"""Compare concurrency models, including pool startup, for local validation."""

import argparse
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from itertools import islice
from statistics import median
from time import perf_counter
from typing import Callable, Union

from turkish_validator import is_valid_turkish_id, is_valid_turkish_tax_no


def _validate_batch(validator: Callable[[str], bool],
                    batch: tuple[str, ...]) -> list[bool]:
    return [validator(number) for number in batch]


async def _validate_async(validator: Callable[[str], bool],
                          batches: list[tuple[str, ...]]) -> list[list[bool]]:

    async def validate(batch: tuple[str, ...]) -> list[bool]:
        # There is no I/O to await: coroutine scheduling cannot parallelize this.
        return _validate_batch(validator, batch)

    return await asyncio.gather(*(validate(batch) for batch in batches))


def _validate_pool(
    pool_type: Union[type[ThreadPoolExecutor], type[ProcessPoolExecutor]],
    workers: int,
    validator: Callable[[str], bool],
    batches: list[tuple[str, ...]],
) -> list[list[bool]]:
    with pool_type(max_workers=workers) as pool:
        return list(pool.map(partial(_validate_batch, validator), batches))


def _positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=_positive_int, default=100_000)
    parser.add_argument("--batch-size", type=_positive_int, default=1_000)
    parser.add_argument("--workers", type=_positive_int, default=4)
    parser.add_argument("--repeat", type=_positive_int, default=3)
    args = parser.parse_args()

    cases = (
        ("ID", is_valid_turkish_id, ("10000000146", "10000000147")),
        ("Tax", is_valid_turkish_tax_no, ("1234567898", "1234567899")),
    )
    print(
        f"{args.count:,} numbers per validator; batch size {args.batch_size:,}; "
        f"{args.workers} workers; median of {args.repeat} runs")
    print("Pool startup, scheduling, and result collection are included.")
    for name, validator, samples in cases:
        numbers = (samples[index % len(samples)] for index in range(args.count))
        batches = []
        while batch := tuple(islice(numbers, args.batch_size)):
            batches.append(batch)
        expected = [_validate_batch(validator, batch) for batch in batches]
        runners: tuple[tuple[str, Callable[[], list[list[bool]]]], ...] = (
            (
                "sequential",
                lambda:
                [_validate_batch(validator, batch) for batch in batches],
            ),
            ("asyncio",
             lambda: asyncio.run(_validate_async(validator, batches))),
            (
                "threads",
                partial(_validate_pool, ThreadPoolExecutor, args.workers,
                        validator, batches),
            ),
            (
                "processes",
                partial(_validate_pool, ProcessPoolExecutor, args.workers,
                        validator, batches),
            ),
        )
        print(f"\n{name}:")
        for model, run in runners:
            elapsed = []
            for _ in range(args.repeat):
                start = perf_counter()
                result = run()
                elapsed.append(perf_counter() - start)
                if result != expected:
                    raise AssertionError(
                        f"{name}: {model} changed validation results")
            seconds = median(elapsed)
            print(
                f"  {model:10} {seconds:.4f}s  {args.count / seconds:,.0f} numbers/s"
            )


if __name__ == "__main__":
    main()
