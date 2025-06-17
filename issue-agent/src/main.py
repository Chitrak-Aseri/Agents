from src.graph.graph_builder import run_autonomous_issue_agent
from src.core.models import ModelFactory
from src.core.config import Config
from src.cli import parse_args

def main():
    args = parse_args()

    # Load and patch config file
    config = Config(skip_yaml=args.skip_yaml)

    # Inject CLI overrides
    config.config["models"] = [{
        "type": args.provider,
        "params": {
            "model_name": args.model_name,
            "openai_api_key": args.api_key,
            "openai_api_base": args.api_base,
        }
    }]

    llm = ModelFactory(config).get_llms()
    run_autonomous_issue_agent(args.src, llm=llm, config=config)

if __name__ == "__main__":
    main()
