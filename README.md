# Python Package Template

[![Release version](https://img.shields.io/badge/dynamic/json?color=green&label=version&query=%24.info.version&url=https%3A%2F%2Ftest.pypi.org%2Fpypi%2Fpysamplelib%2Fjson)](https://test.pypi.org/pypi/pysamplelib)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python version](https://img.shields.io/badge/python-3.10-blue)
![Supported platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows%20%7C%20Linux-green)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Pipeline status](https://github.com/kieran-ryan/python-package-template/actions/workflows/main.yml/badge.svg)

A template repository for creating Python packages.

## Features

- Common repository files:
  - `.gitignore` with common files to be excluded by git for Python
  - `.pre-commit-config.yaml` with automated pre-commit validation for Python
  - `LICENSE` outlining usage rights
  - `Makefile` standardising commands
  - `CODE_OF_CONDUCT.md` outlining community practice
  - `OWNERS.md` outlining owners and roles
  - `README.md` overview documentation
- Tool configuration:
  - [editorconfig](https://editorconfig.org) - universal editor configuration
  - [ruff](https://github.com/charliermarsh/ruff) - linting
  - [perflint](https://github.com/tonybaloney/perflint) - linting performance anti-patterns
  - [mypy](https://mypy.readthedocs.io) - type checking
  - [bandit](https://bandit.readthedocs.io/en/latest/) - vulnerability detection
  - [black](https://black.readthedocs.io/en/stable/) - code style formatting
  - [blacken-docs](https://pypi.org/project/blacken-docs/) - code style formatting in docs
  - [pyupgrade](https://github.com/asottile/pyupgrade) - latest syntax upgrades
  - [radon](https://pypi.org/project/radon/) - code quality
  - [removestar](https://github.com/asmeurer/removestar) - automated removal of wildcard imports (*)
  - [pytest](https://docs.pytest.org) - testing
  - [coverage](https://coverage.readthedocs.io/en/6.2/) - test coverage
  - [sphinx](https://www.sphinx-doc.org/en/master/) - documentation
  - [github-pages](https://pages.github.com) - documentation deployment and hosting
  - [build](https://github.com/pypa/build) - packaging
  - [twine](https://twine.readthedocs.io/en/stable/pip) - deployment
- Examples:
  - Repository tree structure
  - Python module
  - Unit tests

## Installation

`pysamplelib` is available via Test PyPI (via [Platform Wheels](https://packaging.python.org/guides/distributing-packages-using-setuptools/#platform-wheels)):

```
pip install --index-url https://test.pypi.org/simple/ pysamplelib
```

## Examples

Running fizzbuzz against a number:

```python
import pysamplelib

print(pysamplelib.fizzbuzz(5))
```

Running fizzbuzz against a number range:

```python
import pysamplelib

for number in range(1, 101):
    print(pysamplelib.fizzbuzz(number))
```

Running fizzbuzz against a number, using a custom keyword mapping:

```python
import pysamplelib

CUSTOM_KEYWORD_MAPPING = {
    7: "Riff",
    9: "Blip",
}

print(pysamplelib.fizzbuzz(7, CUSTOM_KEYWORD_MAPPING))
```

## License

`pysamplelib` is licensed under the [MIT License](https://opensource.org/licenses/MIT)
