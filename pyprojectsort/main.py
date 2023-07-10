"""pyprojectsort implementation."""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

import tomli as tomllib
import tomli_w

from . import __version__

DEFAULT_CONFIG = "pyproject.toml"


def _read_cli(args: list) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="pyprojectsort",
        description="Formatter for pyproject.toml files",
    )
    parser.add_argument("file", nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="show package version and exit",
    )
    parser.add_argument(
        "--check",
        help=(
            "Don't write the files back, just return the status. Return code 0 means"
            " nothing would change. Return code 1 means the file would be reformatted"
        ),
        action="store_true",
    )
    return parser.parse_args(args)


def _read_config_file(config: pathlib.Path) -> pathlib.Path:
    """Check configuration file exists."""
    if not config.is_file():
        print(f"No pyproject.toml detected at path: '{config}'")
        sys.exit(1)
    return config


def _parse_pyproject_toml(file: pathlib.Path) -> dict[str, Any]:
    """Parse pyproject.toml file."""
    with file.open("r") as pyproject_file:
        return pyproject_file.read()


def reformat_pyproject(pyproject: dict | list) -> dict:
    """Reformat pyproject toml file."""
    if isinstance(pyproject, dict):
        return {
            key: reformat_pyproject(value) for key, value in sorted(pyproject.items())
        }
    if isinstance(pyproject, list):
        numbers = []
        strings = []
        dictionaries = []
        for i in pyproject:
            if isinstance(i, float | int):
                numbers.append(i)
            elif isinstance(i, str):
                strings.append(i)
            else:
                dictionaries.append(reformat_pyproject(i))
        return sorted(numbers, key=lambda x: str(x)) + sorted(strings) + dictionaries
    return pyproject


def _check_format_needed(original: str, reformatted: str) -> bool:
    """Check if there are any differences between original and reformatted."""
    return original != reformatted


def _save_pyproject(file: pathlib.Path, pyproject: dict) -> None:
    """Write changes to pyproject.toml."""
    with file.open("wb") as pyproject_file:
        tomli_w.dump(pyproject, pyproject_file)


def main() -> None:
    """Run application."""
    args = _read_cli(sys.argv[1:])
    pyproject_file = _read_config_file(pathlib.Path(args.file))

    pyproject_toml: str = _parse_pyproject_toml(pyproject_file)
    pyproject: dict = tomllib.loads(pyproject_toml)
    reformatted_pyproject: dict = reformat_pyproject(pyproject)
    reformatted_pyproject_toml: str = tomli_w.dumps(reformatted_pyproject)

    will_reformat = _check_format_needed(pyproject_toml, reformatted_pyproject_toml)

    if args.check:
        if will_reformat:
            print(f"'{args.file}' would be reformatted")
            sys.exit(1)

        print(f"'{args.file}' would be left unchanged")
        return

    if will_reformat:
        _save_pyproject(pyproject_file, reformatted_pyproject)
        print(f"Reformatted '{args.file}'")
        sys.exit(1)

    print(f"'{args.file}' left unchanged")
