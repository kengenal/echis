.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

run:
	poetry run python main.py

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache


test: ## run tests quickly with the default Python
	python -m pytest tests


linter: ## run flake8
	poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=.venv
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=.venv

deps: ## generate requirements.txt from pyproject.toml
	poetry export -f requirements.txt --output requirements.txt
