from langchain.agents import Tool

from src.utils.github import fetch_existing_issues
from src.utils.parser import parse_all_documents


def _parse_docs(_: str) -> str:
    """Parse all documents from the 'data' folder and return as concatenated string.

    Args:
        _: Unused input parameter (required by Tool interface)

    Returns:
        str: All parsed documents joined by newlines
    """
    docs = parse_all_documents("data")
    return "\n".join(docs)


def _fetch_issues(_: str) -> str:
    """Fetch all open GitHub issues and return as concatenated string.

    Args:
        _: Unused input parameter (required by Tool interface)

    Returns:
        str: All open issues joined by newlines
    """
    return "\n".join(fetch_existing_issues())


def return_structured_output(data: str) -> str:
    """Return input data unchanged (intended for JSON output from LLM).

    Args:
        data: The input string (typically JSON) to return

    Returns:
        str: The unmodified input data
    """
    return data  # Return exactly what LLM gives us (ideally valid JSON)


TOOLS = [
    Tool.from_function(
        name="parse_all_documents",
        func=_parse_docs,
        description="Parse all documents from the 'data' folder including JSON, XML, and TXT",
    ),
    Tool.from_function(
        name="fetch_existing_issues",
        func=_fetch_issues,
        description="Fetch all currently open GitHub issues from the configured repository",
    ),
    Tool.from_function(
        name="return_json",
        func=return_structured_output,
        description="Return the final structured output as JSON when you're done analyzing the documents.",
    ),
    # Tool.from_function(
    # name="get_sonar_quality_metrics",
    # func=parse_sonar_report,
    # description="Returns structured SonarQube quality metrics"
    # )
]
