define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
sources = py_cover_letters

.PHONY: test format lint unittest coverage pre-commit clean
test: lint unittest

format:
	isort $(sources) tests
	black $(sources) tests

lint:
	flake8 $(sources) tests
	mypy $(sources) tests

unittest: clean
	pytest

cov:
	pytest --cov=$(sources) --cov-branch --cov-report=term-missing tests
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .mypy_cache .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site
	rm -rf coverage.xml .coverage
	rm -rf output/*.*
	rm -rf output/backups/*.*
	rm -rf output/cli_test/*.*
	rm -rf output/cli_test/output/*.*
