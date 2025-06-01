# Makefile

.PHONY: requirements black isort 

requirements:
	uv export --no-dev --no-hashes > requirements.txt

black:
	uv run black src/ tests/

isort:
	uv run isort src/ tests/

lint-all: black isort 
