"""Package top-level unit tests."""

from __future__ import annotations

import pysamplelib


def test_package():
    """Package top-level contains version information."""
    assert "__version__" in pysamplelib.__all__
