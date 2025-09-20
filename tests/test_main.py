"""pyprojectsort unit tests."""

from __future__ import annotations

import pathlib
import sys
import unittest.mock
from io import StringIO

import pytest
from packaging.version import InvalidVersion, Version

from pyprojectsort.main import (
    _check_format_needed,
    _read_cli,
    _read_config_file,
    main,
    reformat_pyproject,
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
    try:
        Version(output.text)
    except InvalidVersion:
        pytest.fail(f"Invalid version: {output.text}")


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
        "tool.pylint": {"ignore": ["docs", "tests", "venv", 1, 1.1, {}]},
        "tool.black": {"line_length": 88},
    }

    # TODO(@kieran-ryan): Amend test to validate order
    sorted_pyproject = {
        "build-system": {"name": "flit"},
        "project": {"name": "pyprojectsort"},
        "tool.black": {"line_length": 88},
        "tool.pylint": {"ignore": [1, 1.1, "docs", "tests", "venv", {}]},
    }
    assert reformat_pyproject(pyproject) == sorted_pyproject


class CLIArgs:
    """Test class for command line arguments."""

    def __init__(
        self,
        file: str = "test_data.toml",
        check: bool | None = None,
        diff: bool | None = None,
    ):
        """Initialise test data arguments."""
        self.file = file
        self.check = check
        self.diff = diff


@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_main_with_check_and_diff_options(read_cli, read_config):
    """SystemExit with error code if both check and diff CLI options provided."""
    args = CLIArgs(check=True, diff=True)
    read_cli.return_value = args

    with pytest.raises(SystemExit) as reformatted, OutputCapture() as output:
        main()

    assert reformatted.value.code == 1
    assert (
        output.text
        == "Use of 'check' with 'diff' is redundant. Please use one or the other."
    )


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
    save_project,
):
    """Test file reformatted."""
    args = CLIArgs()
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = "change = 1"
    reformat_pyproject.return_value = {"change": 1}

    with pytest.raises(SystemExit) as reformatted, OutputCapture() as output:
        main()

    assert reformatted.value.code == 1
    assert f"Reformatted '{args.file}'" in output.text


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
    args = CLIArgs()
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = ""
    reformat_pyproject.return_value = {}

    with OutputCapture() as output:
        main()

    assert f"'{args.file}' left unchanged" in output.text


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
    args = CLIArgs(check=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = "change = 1"
    reformat_pyproject.return_value = {"change": 1}

    with pytest.raises(SystemExit) as would_reformat, OutputCapture() as output:
        main()

    assert f"'{args.file}' would be reformatted" in output.text
    assert would_reformat.value.code == 1


@pytest.mark.parametrize(
    ("original"),
    [
        ('unsorted = [\n    "tests",\n    "docs",\n]\n'),
        ('not-indented = [\n    "docs",\n"tests",\n]\n'),
        ('no-trailing-comma = [\n    "docs",\n    "tests"\n]\n'),
        ('not-line-per-list-value = ["docs","tests"]\n'),
        ('extra_spaces =   "value"\n'),
        ('no-newline-at-end-of-file = "value"'),
        ("single-quotes = 'value'\n"),
    ],
)
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_check_would_reformat(
    read_cli,
    read_config,
    parse_pyproject,
    original,
):
    """Test --check option when reformat occurs."""
    args = CLIArgs(check=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = original

    with pytest.raises(SystemExit) as would_reformat, OutputCapture() as output:
        main()
    print(output.text)
    assert f"'{args.file}' would be reformatted" in output.text
    assert would_reformat.value.code == 1


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
    args = CLIArgs(check=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = "unchanged = 1\n"
    reformat_pyproject.return_value = {"unchanged": 1}

    with OutputCapture() as output:
        main()

    assert f"'{args.file}' would be left unchanged" in output.text


@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_diff_option_reformat_needed(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
):
    """Test --diff option when reformat occurs."""
    args = CLIArgs(diff=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = "change = 1"
    reformat_pyproject.return_value = {"change": 1}

    with pytest.raises(SystemExit) as would_reformat, OutputCapture() as output:
        main()

    assert f"'{args.file}' would be reformatted" in output.text
    assert would_reformat.value.code == 1


@pytest.mark.parametrize(
    ("original"),
    [
        ('unsorted = [\n    "tests",\n    "docs",\n]\n'),
        ('not-indented = [\n    "docs",\n"tests",\n]\n'),
        ('no-trailing-comma = [\n    "docs",\n    "tests"\n]\n'),
        ('not-line-per-list-value = ["docs","tests"]\n'),
        ('extra_spaces =   "value"\n'),
        ('no-newline-at-end-of-file = "value"'),
        ("single-quotes = 'value'\n"),
    ],
)
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_diff_would_reformat(
    read_cli,
    read_config,
    parse_pyproject,
    original,
):
    """Test --diff option when reformat occurs."""
    args = CLIArgs(diff=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = original

    with pytest.raises(SystemExit) as would_reformat, OutputCapture() as output:
        main()
    print(output.text)
    assert f"'{args.file}' would be reformatted" in output.text
    assert would_reformat.value.code == 1


@unittest.mock.patch("pyprojectsort.main.reformat_pyproject")
@unittest.mock.patch("pyprojectsort.main._parse_pyproject_toml")
@unittest.mock.patch("pyprojectsort.main._read_config_file")
@unittest.mock.patch("pyprojectsort.main._read_cli")
def test_diff_option_reformat_not_needed(
    read_cli,
    read_config,
    parse_pyproject,
    reformat_pyproject,
):
    """Test --diff option when reformat is not needed."""
    args = CLIArgs(diff=True)
    read_cli.return_value = args
    read_config.return_value = pathlib.Path()
    parse_pyproject.return_value = "unchanged = 1\n"
    reformat_pyproject.return_value = {"unchanged": 1}

    with OutputCapture() as output:
        main()

    assert f"'{args.file}' would be left unchanged" in output.text


@pytest.mark.parametrize(
    ("original", "reformatted", "expected_result"),
    [
        (
            '[tool.pylint]\nignore = [\n\t"tests",\n\t"docs",\n]',
            '[tool.pylint]\nignore = [\n\t"tests",\n\t"docs",\n]',
            False,
        ),
        (
            '[tool.pylint]\nignore = [\n\t"tests",\n\t"docs",\n]',
            '[tool.pylint]\nignore = [\n\t"docs",\n\t"tests",\n]',
            True,
        ),
    ],
)
def test_check_format_needed(original, reformatted, expected_result):
    """Test _check_format_needed function with different test cases."""
    assert _check_format_needed(original, reformatted) == expected_result
