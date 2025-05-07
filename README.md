<h1 align="center">pyprojectsort</h1>

<p align="center">
  <b>Formatter for pyproject.toml files</b>
</p>

[![PyPI Version](https://badge.fury.io/py/pyprojectsort.svg)](https://pypi.org/project/pyprojectsort/)
![LICENSE](https://img.shields.io/badge/license-MIT-blue)
[![Python versions](https://img.shields.io/pypi/pyversions/pyprojectsort.svg)](https://pypi.org/pypi/pyprojectsort)
![Supported platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows%20%7C%20Linux-green)
![Pipeline status](https://github.com/kieran-ryan/python-package-template/actions/workflows/main.yml/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/kieran-ryan/pyprojectsort/main.svg)](https://results.pre-commit.ci/latest/github/kieran-ryan/pyprojectsort/main)
[![codecov](https://codecov.io/gh/kieran-ryan/pyprojectsort/graph/badge.svg?token=MNGM4NAXEB)](https://codecov.io/gh/kieran-ryan/pyprojectsort)

This package enforces consistent formatting of pyproject.toml files, reducing merge request conflicts and saving time otherwise spent on manual formatting. It also contributes to a cleaner git history and more readable code; enhancing overall project organisation and maintainability. Experience a streamlined workflow, reduced errors, and improved code readability with `pyprojectsort`.

## Features

- Alphanumerically sorts pyproject.toml by:
    - section
    - section key
    - list value
- Reformats pyproject.toml to a standardised style
    - line per list value
    - double quotations
    - trailing commas
    - indentation
    - end of file newline

## Installation

`pyprojectsort` is available via [PyPI](https://pypi.org/project/pyprojectsort/):

```console
pip install pyprojectsort
```

### Using pyprojectsort with [pre-commit](https://pre-commit.com)

To use as an automated git hook, add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/kieran-ryan/pyprojectsort
  rev: v0.4.0
  hooks:
      - id: pyprojectsort
```

## Examples

With the following `pyproject.toml`:

```toml
[tool.ruff]
ignore = ["G004",
"T201",
    "ANN"
]

[project]
name = 'pyprojectsort'
authors = [
    { name = "Kieran Ryan" },
    "Author Name <author@email.com>",
    {name="Author Name"}
]

[tool.radon]
show_mi = true
exclude = "tests/*,venv/*"
total_average = true
show_complexity = true

[build-system]
build-backend = "flit.buildapi"
requires = ["flit"]
```

Run the package from within its directory:

```console
pyprojectsort
```

The configuration will be reformatted as follows:

```toml
[build-system]
build-backend = "flit.buildapi"
requires = [
    "flit",
]

[project]
authors = [
    "Author Name <author@email.com>",
    { name = "Author Name" },
    { name = "Kieran Ryan" },
]
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

The pyproject file path can alternatively be specified:

```console
pyprojectsort ../pyproject.toml
```

### Check formatting

The **--check** option can be used to determine whether your file would be reformatted.

```console
pyprojectsort --check
```

If the file needs reformatting, the program exits with an error code. This is useful for [pipeline integration](https://github.com/kieran-ryan/pyprojectsort/blob/d9cf5e1e646e1e5260f7cf0168ecd0a05ce8ed11/.github/workflows/main.yml#L30) as it prevents writing back changes so that a clean repository is maintained for subsequent jobs.

The **--diff** option provides similar functionality but also displays any changes that would be made.

```console
pyprojectsort --diff
```

The diff of an alphabetically reordered array will appear as follows:

```diff
@@ -6,8 +6,8 @@
[project]
authors = [
+ { name = "Author Name" },
  { name = "Kieran Ryan" },
- { name = "Author Name" },
]
```

## Contributing

Contributions are welcome for `pyprojectsort`, and can be made by raising [issues](https://github.com/kieran-ryan/pyprojectsort/issues) or [pull requests](https://github.com/kieran-ryan/pyprojectsort/pulls).

Using [`uv`](https://docs.astral.sh/uv/getting-started/installation/#pypi) for package and project management is encouraged when developing with the project - though not required. You will typically want to use the below commands within the project during development.

| Command                   | Purpose                                     |
| ------------------------- | ------------------------------------------- |
| uv run pytest             | 🧪 Run the tests                            |
| uv run pre-commit         | 🔎 Run the linting checks on staged changes |
| uv run pre-commit install | 🕵️‍♀️ Run the linting checks on commit         |
| uv run mkdocs serve       | 📄 Build the documentation                  |
| uv build                  | 📦 Build the package                        |

## License

`pyprojectsort` is licensed under the [MIT License](https://opensource.org/licenses/MIT).
