"""Configuration file for Sphinx documentation."""

from __future__ import annotations

import pathlib
import sys

import tomli as tomllib

# -- Path setup --------------------------------------------------------------

repository_base_dir = pathlib.Path(__file__).parents[2]
source_base_dir = repository_base_dir / "pyprojectsort"

sys.path.insert(0, str(source_base_dir))

# -- Project information -----------------------------------------------------

import __version__  # noqa: E402

with (repository_base_dir / "pyproject.toml").open("rb") as f:
    pyproject_toml = tomllib.load(f)
toml_config = pyproject_toml.get("project")
project_metadata = {
    k.replace("--", "").replace("-", "_"): v for k, v in toml_config.items()
}

project = project_metadata["name"]
authors = project_metadata["authors"]

# The short X.Y.Z version:
version = __version__.__version__

# The full version, including alpha/beta/rc tags:
release = __version__.__version__

# -- General configuration ---------------------------------------------------

# Sphinx extension module names
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.todo",
    "sphinx_mdinclude",
]

# Paths containing templates, relative to this directory.
templates_path = ["_templates"]

# Patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    ".DS_Store",
    "Thumbs.db",
    "_build",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = "furo"

# Paths containing custom static files (such as style sheets), relative
# to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: list[str] = []
