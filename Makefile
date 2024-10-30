setup:
	pip install uv

lint:
	uv run ruff check .
	uv run ruff check --fix .

format:
	uv run ruff format .

ci:
	setup
	lint
	format
