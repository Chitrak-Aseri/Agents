from src.cli import parse_args
from src.core.config import Config
from src.core.models import ModelFactory
from src.graph.graph_builder import run_autonomous_issue_agent


def main():
    """Main entry point for the autonomous issue agent program.
    
    Parses command line arguments, initializes configuration, creates LLM instance,
    and runs the autonomous issue agent with the provided parameters.
    """
    args = parse_args()

    # Initialize configuration with optional YAML skipping
    config = Config(skip_yaml=args.skip_yaml)
    # Set up model configuration from command line arguments
    config.config["models"] = [
        {
            "type": args.provider,
            "params": {
                "model_name": args.model_name,
                "openai_api_key": args.api_key,
                "openai_api_base": args.api_base,
            },
        }
    ]
    # Get LLM instance from ModelFactory
    llm = ModelFactory(config).get_llms()
    # Run the autonomous issue agent with source directory and configuration
    run_autonomous_issue_agent(args.src, llm=llm, config=config)


if __name__ == "__main__":
    main()