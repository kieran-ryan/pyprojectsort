# pyprojectsort

[![Release version](https://badge.fury.io/py/pyprojectsort.svg)](https://pypi.org/project/pyprojectsort/)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python version](https://img.shields.io/badge/python-3.10-blue)
![Supported platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows%20%7C%20Linux-green)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Pipeline status](https://github.com/kieran-ryan/python-package-template/actions/workflows/main.yml/badge.svg)

Formatter for pyproject.toml files.

This package enforces consistent formatting of pyproject.toml files, reducing merge request conflicts and saving time that would otherwise be spent on manual formatting. It also contributes to a cleaner git history and more readable code; enhancing overall project organisation and maintainability. Experience a streamlined workflow, reduced errors, and improved code readability with `pyprojectsort`.

## Features

- Alphabetically sorts pyproject.toml by:
  - section
  - section key
  - list value
- Reformats pyproject.toml to a standardised style

## Installation

`pyprojectsort` is available via PyPI (via [Platform Wheels](https://packaging.python.org/guides/distributing-packages-using-setuptools/#platform-wheels)):

```console
pip install pyprojectsort
```

## Examples

With the following `pyproject.toml` contained inside a directory:

```toml
[tool.ruff]
ignore = [
    "G004",
"T201",
    "ANN",
]

[project]
name = "pyprojectsort"

[tool.radon]
show_mi = true
exclude = "tests/*,venv/*"
total_average = true
show_complexity = true

[build-system]
build-backend = "flit.buildapi"
requires = ["flit"]
```

Run the package from within the directory of the pyproject toml file:

```console
pyprojectsort
```

The configuration will be reformatted as follows:

```toml
[build-system]
build-backend = "flit.buildapi"
requires = ["flit"]

[project]
name = "pyprojectsort"

[tool.radon]
exclude = "tests/*,venv/*"
show_complexity = true
show_mi = true
total_average = true

[tool.ruff]
ignore = [
    "ANN",
    "G004",
    "T201",
]
```

The path to the pyproject toml file can also be specified from the command line:

```console
pyprojectsort ../pyproject.toml
```

### Check formatting

To check whether formatting would be applied to your file you may use the **--check** option.

```console
pyprojectsort --check
```

In case the file would be reformatted you get the output message ```'{file_path}' would be reformatted``` and the program terminates with exit code 1.

If the given file is in a standardised style you get the output message ```'{file_path}' would be left unchanged``` and the program terminates successfully.

## License

`pyprojectsort` is licensed under the [MIT License](https://opensource.org/licenses/MIT)
