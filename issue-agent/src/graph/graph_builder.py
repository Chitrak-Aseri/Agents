from src.utils.parser import parse_all_documents
from src.utils.github import fetch_existing_issues
from src.agents.generator_agent import run_generator_agent
from src.core.models import ModelFactory
from src.utils.config_loader import load_config
from src.agents.reviewer_agent import run_reviewer_agent


def run_autonomous_issue_agent(data_folder, llm=None, config=None):
    docs = parse_all_documents(data_folder)
    issues = fetch_existing_issues()
    print("************************EXISITING ISSUES*********************************")
    print(issues)
    print("************************EXISITING ISSUES*********************************")

    # fallback if not passed (for backwards compatibility)
    if config is None:
        config = load_config()
    if llm is None:
        llm = ModelFactory(config).get_llms()

    decision = run_reviewer_agent(docs, issues, llm)
    run_generator_agent(decision)
