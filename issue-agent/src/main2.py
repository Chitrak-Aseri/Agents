from langchain_openai import ChatOpenAI
from src.tools.sonar_metrics import summarize_sonar
from src.tools.github_issues import fetch_existing_issues
from src.tools.issue_creator import create_issue
from src.graph.langgraph_runner import build_multi_agent_issue_graph
def main():
    # tools = [summarize_sonar, fetch_existing_issues, create_issue]
    tools = [fetch_existing_issues, summarize_sonar, create_issue]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    graph = build_multi_agent_issue_graph(llm, tools)

    result = graph.invoke({
        "input": """
            You are an autonomous reviewer AI designed to assist in managing GitHub issues effectively.
            Your objective is to analyze the provided documents and the list of currently open GitHub issues to determine whether any **new and non-redundant** issues should be created.

            ### Instructions:

            1. Carefully compare the documents and SonarQube metrics against the current issues.
            2. Identify **gaps, untracked problems, or opportunities for improvement** that are **not already covered** by any existing issue.
            3. Avoid creating duplicate or overlapping issues — each suggested issue must represent a **unique and clearly distinct concern**.
            4. Group similar observations under a single cohesive issue where applicable to reduce noise.
            5. Ensure each new issue has a **concise, descriptive title** and a **clear, actionable description**.
            6. Avoid vague or generic issues; be specific about the problem and its context.
            7. If no new issues are needed, return `create_issues=False` and an empty list for `ISSUES`.
            8. If new issues are needed, return `create_issues=True` and list all new issues under the key `ISSUES`.
            9. Issues must always be unique and not overlap with existing issues.

        """
    })

    print("✅ Result:", result)

if __name__ == "__main__":
    main()
