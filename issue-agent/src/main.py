from src.graph.graph_builder import run_autonomous_issue_agent
from src.core.config import Config
from src.core.models import ModelFactory


def main():
    config = Config()
    llm = ModelFactory(config).get_model()
    run_autonomous_issue_agent("data", llm=llm, config=config)
    
if __name__ == "__main__":
    run_autonomous_issue_agent("data")