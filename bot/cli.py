# bot/cli.py
import argparse
from bot.pipeline import run_commenting_pipeline
from bot.utils.config_loader import load_config


def main():
    parser = argparse.ArgumentParser(description="Auto-comment code using LLMs")

    # Config fallback
    parser.add_argument("--config", help="YAML config file path")

    # Generic model config overrides
    parser.add_argument("--provider", help="LLM provider (e.g. deepseek, openai, bedrock)")
    parser.add_argument("--model_name", help="Model name")
    parser.add_argument("--region", help="Region (for bedrock)")
    parser.add_argument("--api_key", help="API key for providers like OpenAI/DeepSeek")
    parser.add_argument("--api_base", help="Custom API base (for DeepSeek)")
    parser.add_argument("--aws_access_key_id", help="AWS Access Key ID (for Bedrock)")
    parser.add_argument("--aws_secret_access_key", help="AWS Secret Access Key (for Bedrock)")

        # bot/cli.py
    parser.add_argument(
        "--src", nargs="+", default=["./src"], help="Source code folder(s). Space-separated."
    )


    args = parser.parse_args()

    config = load_config(args.config) if args.config else None

    # Only override if provider is passed (so config fallback works)
    if args.provider:
        config = {
            "model": {
                "provider": {
                    "type": args.provider,
                },
                "model_name": args.model_name,
                "region": args.region,
                "credentials": {
                    "api_key": args.api_key,
                    "api_base": args.api_base,
                    "aws_access_key_id": args.aws_access_key_id,
                    "aws_secret_access_key": args.aws_secret_access_key,
                },
            }
        }

    run_commenting_pipeline(
        config=config,
        model_name=args.model_name,  # fallback for legacy
        src_folder=args.src
    )

if __name__ == "__main__":
    main()