test:
	poetry run pytest -s -vv --cov=callable_tm

tests: test

test-coverage:
	poetry run pytest -s -vv --cov=callable_tm --cov-report=xml

isort:
	poetry run isort .

lint:
	ruff check

force-lint:
	ruff check --fix

format:
	ruff format

docs:
	poetry run mkdocs serve
