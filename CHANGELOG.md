# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

### Added

- Python 3.12 support - [#70](https://github.com/kieran-ryan/pyprojectsort/pull/70)

## 0.3.0 - 2023-07-18

### Added

- Command line option to render diff of changes - [#16](https://github.com/kieran-ryan/pyprojectsort/issues/16)
- Official support for Python 3.7 to 3.11 - [#14](https://github.com/kieran-ryan/pyprojectsort/issues/14)

### Changed

- Format mixed data types in an array - [#39](https://github.com/kieran-ryan/pyprojectsort/issues/39)
- Natural sort of string based numbers - [#52](https://github.com/kieran-ryan/pyprojectsort/pull/52)

## 0.2.2 - 2023-07-08

### Added

- Pre-commit git hook support - [#13](https://github.com/kieran-ryan/pyprojectsort/issues/13)

### Fixes

- Write changes when values are the same but formatting required - [#34](https://github.com/kieran-ryan/pyprojectsort/issues/34)

## 0.2.1 - 2023-07-05

### Deprecated

- Key normalisation, which can affect tools that expect a particular format - [#27](https://github.com/kieran-ryan/pyprojectsort/issues/27)

## 0.2.0 - 2023-07-05

### Added

- Support to check whether file would be reformatted without writing changes - [#10](https://github.com/kieran-ryan/pyprojectsort/issues/10)
- Support to specify the pyproject.toml path - [#9](https://github.com/kieran-ryan/pyprojectsort/issues/9)

### Changes

- Alphabetically sort section keys - [#5](https://github.com/kieran-ryan/pyprojectsort/issues/5)
- Alphabetically sort list key values - [#7](https://github.com/kieran-ryan/pyprojectsort/issues/7)

### Fixes

- Writes to pyproject.toml only if there are changes to made - [#19](https://github.com/kieran-ryan/pyprojectsort/pull/19)

## 0.1.1 - 2023-06-26

### Changes

- Alphabetically sort pyproject.toml files by parent section name
