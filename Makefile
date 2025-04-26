test:
	poetry run pytest -s

tests: test

lint:
	ruff check

force-lint:
	ruff check --fix

format:
	ruff format
