# Makefile

.PHONY: requirements black isort  openai deepseek lint-all

requirements:
	uv export --no-dev --no-hashes > requirements.txt

black:
	uv run black src/ 

isort:
	uv run isort src/ 

openai:
	uv run python -m src.main --src="./data/" --provider="openai" --model_name="gpt-4o-mini" --api_key=${OPENAI_API_KEY} --skip-yaml true

deepseek:
	uv run python -m src.main --src="./data/" --provider="deepseek" --model_name="deepseek-chat" --api_key=${DEEPSEEK_API_KEY} --api_base="https://api.deepseek.com/v1" --skip-yaml true

lint-all: black isort 
