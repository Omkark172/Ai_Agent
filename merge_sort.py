"""Merge Sort implementation with validation and structured logging."""
from __future__ import annotations

import logging
from typing import Iterable, List, Sequence, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def merge_sort(values: Sequence[T]) -> List[T]:
    """Return a new list containing the values sorted using merge sort.

    Time complexity: O(n log n)
    Space complexity: O(n)

    Args:
        values: A sequence of comparable values.

    Returns:
        A sorted list containing the values from the input sequence.

    Raises:
        TypeError: If the input is not a sequence.
    """
    if not isinstance(values, Sequence):
        raise TypeError("merge_sort requires a sequence input")

    if len(values) <= 1:
        logger.debug("Base case reached with values=%s", values)
        return list(values)

    mid_index = len(values) // 2
    left_half = merge_sort(values[:mid_index])
    right_half = merge_sort(values[mid_index:])
    merged_result = _merge(left_half, right_half)
    logger.debug("Merged %s and %s into %s", left_half, right_half, merged_result)
    return merged_result


def _merge(left: List[T], right: List[T]) -> List[T]:
    """Merge two sorted input lists and return a new sorted list."""
    merged: List[T] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    if left_index < len(left):
        merged.extend(left[left_index:])
    if right_index < len(right):
        merged.extend(right[right_index:])

    return merged


def parse_values(values: Iterable[str]) -> List[int]:
    """Parse an iterable of strings into a list of integers."""
    parsed: List[int] = []
    for value in values:
        try:
            parsed.append(int(value))
        except ValueError as exc:
            logger.error("Invalid integer value: %s", value)
            raise ValueError(f"Invalid integer value: {value}") from exc
    return parsed


def main() -> None:
    """Run merge sort on command-line arguments and print the sorted output."""
    import sys

    if len(sys.argv) <= 1:
        logger.info("Usage: python merge_sort.py 5 3 8 1")
        return

    numbers = parse_values(sys.argv[1:])
    sorted_numbers = merge_sort(numbers)
    print("Sorted:", sorted_numbers)


if __name__ == "__main__":
    main()
