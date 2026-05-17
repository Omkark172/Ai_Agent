"""Unit tests for merge_sort.py."""

import pytest

from merge_sort import merge_sort, parse_values


@pytest.mark.parametrize(
    "input_values, expected",
    [
        ([], []),
        ([1], [1]),
        ([3, 1, 2], [1, 2, 3]),
        ([5, -1, 3, 0], [-1, 0, 3, 5]),
        ([2, 2, 2], [2, 2, 2]),
    ],
)
def test_merge_sort_happy_path(input_values, expected):
    assert merge_sort(input_values) == expected


def test_merge_sort_with_strings_sorted_lexicographically():
    assert merge_sort(["c", "a", "b"]) == ["a", "b", "c"]


def test_merge_sort_invalid_input_type_raises_type_error():
    with pytest.raises(TypeError):
        merge_sort(123)  # type: ignore[arg-type]


def test_parse_values_valid_strings():
    assert parse_values(["4", "0", "-5"]) == [4, 0, -5]


def test_parse_values_invalid_string_raises_value_error():
    with pytest.raises(ValueError, match="Invalid integer value"):
        parse_values(["1", "abc", "3"])
