from langchain_openai import ChatOpenAI
from src.tools.sonar_metrics import parse_sonar_metrics
from src.tools.github_issues import fetch_existing_issues
from src.tools.issue_creator import create_issue
from src.tools.codebase_fetcher import fetch_codebase
from src.graph.langgraph_runner import build_multi_agent_issue_graph


from src.utils.parser import parse_all_documents

from src.utils.parser import parse_all_documents

def main():
    tools = [fetch_existing_issues, parse_sonar_metrics, create_issue, fetch_codebase]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    graph = build_multi_agent_issue_graph(llm, tools)

    parsed = parse_all_documents("data")
    full_prompt = f"""
    You are an autonomous reviewer AI designed to assist in managing GitHub issues effectively.
    Your objective is to analyze the provided documents and the list of currently open GitHub issues to determine whether any **new and non-redundant** issues should be created.

    {parsed['llm_text']}

    ### Instructions:

    1. Carefully compare the documents and SonarQube metrics against the current issues.
    2. Identify **gaps, untracked problems, or opportunities for improvement** that are **not already covered** by any existing issue.
    3. Avoid creating duplicate or overlapping issues — each suggested issue must represent a **unique and clearly distinct concern**.
    4. Group similar observations under a single cohesive issue where applicable to reduce noise.
    5. Ensure each new issue has a **concise, descriptive title** and a **clear, actionable description**.
    6. If no new issues are needed, return `create_issues=False` and an empty list for `ISSUES`.
    7. Make sure issues are actionable and specific, avoiding vague or generic descriptions, and have context to the codebase. For that utilize `fetchcodebase` tool to fetch the codebase files and their content.
    8. If new issues are needed, return `create_issues=True` and list all new issues under the key `ISSUES`. Example:
        {{
            "create_issues": true,
            "ISSUES": [
                {{
                    "title": "Low Test Coverage in Core Module",
                    "body": "Test coverage is 45% in src/core/config.py. Improve this to at least 80% to meet the project standards."
                }}
            ]
        }}
    """

    result = graph.invoke({"input": full_prompt})
    print("✅ Result:", result)

if __name__ == "__main__":
    main()
