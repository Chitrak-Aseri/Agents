from src.core.models import ModelFactory
from src.core.config import Config
from src.cli import parse_args
from src.utils.parser import parse_all_documents
from src.agents.reviewer_agent import run_reviewer_agent
from src.utils.github import fetch_existing_issues
from src.agents.generator_agent import run_generator_agent

def main():
    args = parse_args()


    config = Config(skip_yaml=args.skip_yaml)
    config.config["models"] = [{
        "type": args.provider,
        "params": {
            "model_name": args.model_name,
            "openai_api_key": args.api_key,
            "openai_api_base": args.api_base,
        }
    }]

    
    llms = ModelFactory(config).get_llms()

    
   
    
    existing_gh_issues = fetch_existing_issues()
    parsed_result = parse_all_documents(args.src)  


   
    reviewer_result = run_reviewer_agent(parsed_input=parsed_result, issues=existing_gh_issues, llms=llms)

   

    run_generator_agent(reviewer_result)

if __name__ == "__main__":
    main()
