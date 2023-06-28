"""pyprojectsort implementation."""
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
    if isinstance(pyproject, dict):
        return {
            key: reformat_pyproject(value)
            for key, value in sorted(pyproject.items(), key=lambda item: item[0])
        }
    if isinstance(pyproject, list):
        return [reformat_pyproject(item) for item in pyproject]
    return pyproject


def main():
    """Run application."""
    data_dict = reformat_pyproject(pyproject_toml)
    with pathlib.Path("pyproject.toml").open("wb") as f:
        tomli_w.dump(data_dict, f)
