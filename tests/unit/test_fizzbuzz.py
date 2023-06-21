"""FizzBuzz unit tests."""

from __future__ import annotations

import pytest

from pysamplelib.fizzbuzz import fizzbuzz


@pytest.mark.parametrize(
    ("number", "output"),
    [
        (2, "2"),
        (3, "Fizz"),
        (3.0, "Fizz"),
        (3.5, "3.5"),
        (5, "Buzz"),
        (5.0, "Buzz"),
        (6, "Fizz"),
        (7, "7"),
        (9, "Fizz"),
        (10, "Buzz"),
        (11, "11"),
        (14, "14"),
        (15, "FizzBuzz"),
        (15.0, "FizzBuzz"),
        (18, "Fizz"),
        (20, "Buzz"),
        (25, "Buzz"),
        (30, "FizzBuzz"),
        (45, "FizzBuzz"),
        (60, "FizzBuzz"),
    ],
)
def test_fizzbuzz_default(number, output):
    """Test `fizzbuzz` function with default keyword mapping."""
    print("testing", number)
    assert fizzbuzz(number) == output


@pytest.mark.parametrize(
    ("number", "output"),
    [
        (2, "2"),
        (3.5, "3.5"),
        (4, "Biff"),
        (4.0, "Biff"),
        (7, "7"),
        (8, "Biff"),
        (9, "Fuzz"),
        (9.0, "Fuzz"),
        (11, "11"),
        (14, "14"),
        (12, "Biff"),
        (16, "Biff"),
        (18, "Fuzz"),
        (27, "Fuzz"),
        (36, "BiffFuzz"),
        (36.0, "BiffFuzz"),
        (45, "Fuzz"),
        (72, "BiffFuzz"),
        (108, "BiffFuzz"),
        (144, "BiffFuzz"),
    ],
)
def test_fizzbuzz_custom(number, output):
    """Test `fizzbuzz` function with custom keyword mapping."""
    custom_keywords = {
        4: "Biff",
        9: "Fuzz",
    }

    print("testing", number)
    assert fizzbuzz(number, custom_keywords) == output
