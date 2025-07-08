# Makefile

.PHONY: requirements black isort run-cli-only-deepseek run-cli-only-openai

requirements:
	poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt 

black:
	uv run black src/ tests/

isort:
	uv run isort src/ tests/

run-cli-only-deepseek:
	poetry run python -m bot.cli --provider deepseek  --model_name deepseek-chat --api_key $DEEPSEEK_API_KEY --api_base https://api.deepseek.com/v1 --src ./src/game/  

run-cli-only-openai:
	poetry run python -m bot.cli --provider openai --model_name gpt-4o-mini --api_key $OPENAI_API_KEY --src ./src/game/ 

lint-all: black isort 