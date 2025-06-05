# Makefile

.PHONY: requirements black isort 

requirements:
	uv export --no-dev --no-hashes > requirements.txt

black:
	uv run black src/ tests/

isort:
	uv run isort src/ tests/

run-cli:
	uv run python -m src.main --config ai-reviewer.yaml 

lint-all: black isort 
