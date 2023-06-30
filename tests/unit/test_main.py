"""pyprojectsort unit tests."""

from __future__ import annotations

import pathlib
import sys
import unittest.mock
from io import StringIO

import pytest

from pyprojectsort import __version__
from pyprojectsort.main import _read_cli, _read_config_file, main, reformat_pyproject


def test_default_filename():
    """Check expected default pyproject filename."""
    assert _read_cli([]).file == "pyproject.toml"


def test_version():
    """Program successfully displays package version and exits."""
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as version:
        _read_cli(["--version"])
    sys.stdout = sys.__stdout__
    assert version.value.code == 0
    assert captured_output.getvalue().strip("\n") == __version__


def test_invalid_config_file_path():
    """SystemExit raised if config file path does not exist."""
    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit) as invalid_config:
        _read_config_file(pathlib.Path("test_data.toml"))
    sys.stdout = sys.__stdout__
    assert invalid_config.value.code == 1
    assert (
        captured_output.getvalue().strip("\n")
        == "No pyproject.toml detected at path: 'test_data.toml'"
    )


@unittest.mock.patch("pathlib.Path.is_file")
def test_valid_config_file_path(is_file):
    """Test a valid file path is provided."""
    is_file.return_value = True
    file_path = pathlib.Path("test_data.toml")
    assert _read_config_file(file_path) == file_path


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


class TestArgs:
    """Test class for command line arguments."""

    file = "test_data.toml"


@unittest.mock.patch("pyprojectsort.main._save_pyproject")
@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_main(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
    save_pyproject,
):
    """Test main application function."""
    read_cli.return_value = TestArgs()
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = {}
    reformat_pyproject.return_value = {}
    main()
