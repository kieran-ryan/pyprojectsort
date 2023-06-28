"""pyprojectsort unit tests."""

from __future__ import annotations

from pyprojectsort.main import reformat_pyproject


def test_reformat_pyproject():
    """Test pyproject toml is reformatted."""
    pyproject = {
        "project": {"name": "pyprojectsort"},
        "build-system": {"name": "flit"},
        "tool.pylint": {"ignore": ["docs", "tests", "venv"]},
        "tool.black": {"line_length": 88},
    }

    # TODO: Amend test to validate order
    sorted_pyproject = {
        "build-system": {"name": "flit"},
        "project": {"name": "pyprojectsort"},
        "tool.black": {"line_length": 88},
        "tool.pylint": {"ignore": ["docs", "tests", "venv"]},
    }
    assert reformat_pyproject(pyproject) == sorted_pyproject
