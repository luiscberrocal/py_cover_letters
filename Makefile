sources = py_cover_letters

.PHONY: test format lint unittest coverage pre-commit clean
test: lint unittest

format:
	isort $(sources) tests
	black $(sources) tests

lint:
	flake8 $(sources) tests
	mypy $(sources) tests

unittest:
	pytest

coverage:
	pytest --cov=$(sources) --cov-branch --cov-report=term-missing tests

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
