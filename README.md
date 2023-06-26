# pyproject-sort

[![Release version](https://img.shields.io/badge/dynamic/json?color=green&label=version&query=%24.info.version&url=https%3A%2F%2Ftest.pypi.org%2Fpypi%2Fpyprojectsort%2Fjson)](https://test.pypi.org/pypi/pyprojectsort)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python version](https://img.shields.io/badge/python-3.10-blue)
![Supported platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows%20%7C%20Linux-green)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Pipeline status](https://github.com/kieran-ryan/python-package-template/actions/workflows/main.yml/badge.svg)

Autoformatter for pyproject.toml files.

Ensures pyproject.toml files are consistently formatted; preventing merge request conflicts, reducing time spent manually formatting; and maintaining a cleaner git history and readability.

## Features

- Alphabetically sorts pyproject.toml by parent section name

## Installation

`pyprojectsort` is available via Test PyPI (via [Platform Wheels](https://packaging.python.org/guides/distributing-packages-using-setuptools/#platform-wheels)):

```console
pip install pyprojectsort
```

## Examples

With the following `pyproject.toml` contained inside a directory:

```toml
[project]
name = "pyprojectsort"

[build-system]
build-backend = "flit.buildapi"
requires = ["flit"]
```

Run the package from within the directory of the pyproject toml file as follows:

```console
pyprojectsort
```

`pyprojectsort` will reformat the `pyproject.toml` to the alphabetical order of the sections:

```toml
[build-system]
build-backend = "flit.buildapi"
requires = ["flit"]

[project]
name = "pyprojectsort"
```

## License

`pyprojectsort` is licensed under the [MIT License](https://opensource.org/licenses/MIT)
