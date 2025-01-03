"""Package top-level unit tests."""

from __future__ import annotations

import pyprojectsort


def test_package():
    """Package top-level contains version information."""
    assert "__version__" in pyprojectsort.__all__
