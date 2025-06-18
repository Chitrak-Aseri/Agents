from src.agents.generator_agent import run_generator_agent
from src.agents.reviewer_agent import run_reviewer_agent
from src.core.models import ModelFactory
from src.utils.config_loader import load_config
from src.utils.github import fetch_existing_issues
from src.utils.parser import parse_all_documents


def run_autonomous_issue_agent(data_folder, llm=None, config=None):
    """Run the autonomous issue agent pipeline to process documents and manage GitHub issues.

    Args:
        data_folder (str): Path to folder containing documents to parse.
        llm (optional): Pre-initialized language model instance. Defaults to None.
        config (optional): Configuration dictionary. Defaults to None.

    The pipeline:
    1. Parses all documents in data_folder
    2. Fetches existing GitHub issues
    3. Uses reviewer agent to analyze documents vs existing issues
    4. Runs generator agent based on reviewer's decision
    """
    docs = parse_all_documents(data_folder)
    issues = fetch_existing_issues()
    print("************************EXISITING ISSUES*********************************")
    print(issues[:100])  # Print only the first 1000 characters for brevity
    print("************************EXISITING ISSUES*********************************")

    # fallback if not passed (for backwards compatibility)
    if config is None:
        config = load_config()
    if llm is None:
        llm = ModelFactory(config).get_llms()

    decision = run_reviewer_agent(parsed_input=docs, issues=issues, llms=llm)
    run_generator_agent(decision)