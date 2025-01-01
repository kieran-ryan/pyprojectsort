.PHONY: docs
init:
	python -m venv venv
	. venv/bin/activate && pip install --requirement requirements.txt

coverage:
	pytest --cov-report term --cov-report html --cov-report xml --cov=pyprojectsort

build:
	pip install build
	python -m build

docs:
	cd docs && make html
