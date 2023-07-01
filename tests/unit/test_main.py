"""pyprojectsort unit tests."""

from __future__ import annotations

import pathlib
import sys
import unittest.mock
from io import StringIO

import pytest

from pyprojectsort import __version__
from pyprojectsort.main import (
    _read_cli,
    _read_config_file,
    main,
    reformat_pyproject,
    _check_format_needed,
)


class OutputCapture:
    """Context manager to capture console output."""

    def __init__(self) -> None:
        """Initialise context manager."""
        self.text = StringIO()

    def __enter__(self):
        """Enter context manager."""
        sys.stdout = self.text
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Exit context manager."""
        sys.stdout = sys.__stdout__
        self.text = self.text.getvalue().strip("\n")


def test_default_filename():
    """Check expected default pyproject filename."""
    assert _read_cli([]).file == "pyproject.toml"


def test_version():
    """Program successfully displays package version and exits."""
    with pytest.raises(SystemExit) as version, OutputCapture() as output:
        _read_cli(["--version"])

    assert version.value.code == 0
    assert output.text == __version__


def test_invalid_config_file_path():
    """SystemExit raised if config file path does not exist."""
    with pytest.raises(SystemExit) as invalid_config, OutputCapture() as output:
        _read_config_file(pathlib.Path("test_data.toml"))

    assert invalid_config.value.code == 1
    assert output.text == "No pyproject.toml detected at path: 'test_data.toml'"


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

    def __init__(self, file: str = "test_data.toml", check: bool = None):
        self.file = file
        self.check = check


@unittest.mock.patch("pyprojectsort.main._save_pyproject")
@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_main_with_file_reformatted(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
    save_pyproject,
):
    """Test file reformatted."""
    args = TestArgs()
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = {}
    reformat_pyproject.return_value = {"change": 1}

    with pytest.raises(SystemExit) as reformatted, OutputCapture() as output:
        main()

    assert reformatted.value.code == 1
    assert output.text == f"Reformatted '{args.file}'"


@unittest.mock.patch("pyprojectsort.main._save_pyproject")
@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_main_with_file_unchanged(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
    save_pyproject,
):
    """Test file left unchanged."""
    args = TestArgs()
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = {}
    reformat_pyproject.return_value = {}

    with OutputCapture() as output:
        main()

    assert output.text == f"'{args.file}' left unchanged"


@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_check_option_reformat_needed(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
):
    """Test --check option when reformat occurs."""
    args = TestArgs(check=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = {}
    reformat_pyproject.return_value = {"change": 1}

    with pytest.raises(SystemExit) as pytest_wrapped_e, OutputCapture() as output:
        main()

    assert output.text == f"'{args.file}' would be reformatted"
    assert pytest_wrapped_e.value.code == 1


@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_check_option_reformat_not_needed(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
):
    """Test --check option when reformat is not needed."""
    args = TestArgs(check=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = {"unchanged": 1}
    reformat_pyproject.return_value = {"unchanged": 1}

    with OutputCapture() as output:
        main()

    assert output.text == f"'{args.file}' would be left unchanged"


@pytest.mark.parametrize(
    ("original", "reformatted", "expected_result"),
    [
        ({"unchanged": 1}, {"unchanged": 1}, False),
        ({"should_be_changed": 1}, {"changed": 1}, True),
    ],
)
def test_check_format_needed(original, reformatted, expected_result):
    """Test _check_format_needed function with different test cases."""
    assert _check_format_needed(original, reformatted) == expected_result
