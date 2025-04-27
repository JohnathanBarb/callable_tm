test:
	poetry run pytest -s -vv --cov=callable_tm

tests: test

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
