import json
import os

from dotenv import load_dotenv
from github import Github
from langchain_core.tools import tool

load_dotenv()


@tool
def parse_sonar_metrics(input: str) -> str:
    """
    Analyze SonarQube metrics and return issue suggestions based on low test coverage.
    Input must be a JSON string with the sonar metrics data.
    """
    try:
        sonar_data = json.loads(input)
        issues = []

        coverage = next(
            (
                m.get("value")
                for m in sonar_data.get("metrics", [])
                if m.get("metric") == "coverage"
            ),
            None,
        )

        if coverage:
            coverage_float = float(coverage)
            if coverage_float < 80:
                issues.append(
                    {
                        "title": "Low Test Coverage",
                        "body": f"Test coverage is below threshold: {coverage_float}%. Please improve test coverage to at least 80%.",
                    }
                )

        if not issues:
            return "No issues detected from sonar metrics."

        return json.dumps({"create_issues": True, "ISSUES": issues})

    except Exception as e:
        return f"Error parsing sonar input: {e}"
