import os

import nest_asyncio
from IPython.display import Image, display
# from langgraph.graph.visualize import draw_mermaid
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_openai import ChatOpenAI

from src.graph.langgraph_runner import build_multi_agent_issue_graph, get_graph_dot_string
from src.tools.codebase_fetcher import fetch_codebase
from src.tools.github_issues import fetch_existing_issues
from src.tools.issue_creator import create_issue
from src.tools.parser import parse_all_documents
from src.tools.sonar_metrics import parse_sonar_metrics


def visualize_graph(graph):
    nest_asyncio.apply()
    image = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.PYPPETEER,
        output_file_path="langgraph_diagram.png",
    )
    display(Image("langgraph_diagram.png"))


def main():
    tools = [
        fetch_existing_issues,
        parse_sonar_metrics,
        create_issue,
        fetch_codebase,
        parse_all_documents,
    ]
    # All tools
    all_tools = [
        fetch_existing_issues,
        parse_sonar_metrics,
        create_issue,
        fetch_codebase,
    ]

    # 🧠 Tools for reviewer (NO create_issue!)
    reviewer_tools = [fetch_existing_issues, parse_sonar_metrics, parse_all_documents]

    # ⚙️ Tools for generator, if needed (not used here, as it creates issues manually)
    generator_tools = [
        create_issue
    ]  # Just FYI; not actually used in your `generator_node`

    llm = ChatOpenAI(
        model_name="deepseek-chat",
        temperature=0.5,
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key=os.environ["DEEPSEEK_API_KEY"],
    )
    builder = build_multi_agent_issue_graph(llm, reviewer_tools, compile_graph=False)
    graph = build_multi_agent_issue_graph(llm, reviewer_tools, compile_graph=True)
    # with open("graph.dot", "w") as f:
    #     f.write(get_graph_dot_string(llm, tools))
    visualize_graph(graph)
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
