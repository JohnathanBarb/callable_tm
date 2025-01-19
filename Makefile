test:
	uv run --all-groups pytest -s

tests: test

lint:
	uv run --all-groups ruff check

force-lint:
	uv run --all-groups ruff check --fix

format:
	uv run --all-groups ruff format
