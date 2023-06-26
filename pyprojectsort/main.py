"""pyproject-sort implementation."""
from __future__ import annotations

import pathlib

import tomli as tomllib
import tomli_w

with pathlib.Path("pyproject.toml").open("rb") as f:
    pyproject_toml = tomllib.load(f)
toml_config = pyproject_toml.get("project")
project_metadata = {
    k.replace("--", "").replace("-", "_"): v for k, v in toml_config.items()
}


def reformat_pyproject(pyproject: dict) -> dict:
    """Reformat pyproject toml file."""
    sections_sorted = sorted(pyproject)
    return {i: pyproject[i] for i in sections_sorted}


sections_sorted = sorted(pyproject_toml)
data_dict = {i: pyproject_toml[i] for i in sections_sorted}

with pathlib.Path("pyproject.toml").open("wb") as f:
    tomli_w.dump(data_dict, f)


def main():
    """Run application."""
    reformat_pyproject(pyproject_toml)
