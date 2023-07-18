"""pyprojectsort implementation."""
from __future__ import annotations

import argparse
import pathlib
import sys
from difflib import unified_diff
from typing import Any

import natsort
import tomli as tomllib
import tomli_w

from . import __version__

DEFAULT_CONFIG = "pyproject.toml"


def _bubble_sort(array: list[dict | list]) -> list[dict | list]:
    """Bubble sort algorithm for sorting an array of lists or dictionaries.

    Examples:
        >>> _bubble_sort([[4, 3], [1, 2]])
        [[1, 2], [4, 3]]
        >>> _bubble_sort([[1.0, 3, 4], ["1", 2]])
        [['1', 2], [1.0, 3, 4]]
        >>> _bubble_sort([{"b": 1}, {"a": 2}])
        [{'a': 2}, {'b': 1}]
        >>> _bubble_sort([{"a": 2}, {"a": 1}])
        [{'a': 1}, {'a': 2}]
        >>> _bubble_sort([{"a": 1}, {"a": 2}])
        [{'a': 1}, {'a': 2}]
        >>> _bubble_sort([])
        []
    """
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            first = get_comparison_array(array[j])
            second = get_comparison_array(array[j + 1])

            if first == second:
                first = get_comparison_array(array[j], values=True)
                second = get_comparison_array(array[j + 1], values=True)

            if first > second:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False

        if already_sorted:
            break
    return array


def get_comparison_array(
    items: list | dict,
    values: bool = False,  # noqa: FBT001, FBT002
) -> list[str]:
    """Returns an array from an iterable to be used for comparison.

    Dictionary keys are returned by default, and values if specified.

    Examples:
        >>> get_comparison_array([2, 4, 5])
        ['2', '4', '5']
        >>> get_comparison_array({"a": 1, "b": 2})
        ['a', 'b']
        >>> get_comparison_array({"a": 1, "b": 2}, values=True)
        ['1', '2']
    """
    if isinstance(items, dict):
        items = items.values() if values else items.keys()
    return list(map(str, items))


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
    parser.add_argument(
        "--diff",
        help="Don't write the files back, just output a diff of changes",
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
            key: reformat_pyproject(value)
            for key, value in natsort.natsorted(pyproject.items())
        }
    if isinstance(pyproject, list):
        data_types = {bool: [], float: [], int: [], str: [], list: [], dict: []}

        def update_data_type(item: Any) -> None:
            """Populate data types map based on item type."""
            data_type = type(item)
            container = data_types[data_type]
            container.append(reformat_pyproject(item))

        list(map(update_data_type, pyproject))

        return (
            data_types[bool]
            + sorted(data_types[int] + data_types[float], key=float)
            + natsort.natsorted(data_types[str])
            + _bubble_sort(data_types[list])
            + _bubble_sort(data_types[dict])
        )
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

    if args.diff and args.check:
        print("Use of 'check' with 'diff' is redundant. Please use one or the other.")
        sys.exit(1)

    pyproject_toml: str = _parse_pyproject_toml(pyproject_file)
    pyproject: dict = tomllib.loads(pyproject_toml)
    reformatted_pyproject: dict = reformat_pyproject(pyproject)
    reformatted_pyproject_toml: str = tomli_w.dumps(reformatted_pyproject)

    will_reformat = _check_format_needed(pyproject_toml, reformatted_pyproject_toml)

    if args.diff:
        if will_reformat:
            for line in unified_diff(
                pyproject_toml.split("\n"),
                reformatted_pyproject_toml.split("\n"),
            ):
                print(line)
            print(f"\n'{args.file}' would be reformatted")
            sys.exit(1)
        print(f"'{args.file}' would be left unchanged")
        return

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
