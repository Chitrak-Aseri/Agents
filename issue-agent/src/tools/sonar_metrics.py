from langchain_core.tools import tool  # ✅ CORRECT
import json

@tool
def summarize_sonar(input: str = "") -> str:
    """Summarize SonarQube metrics into a short report."""
    with open("data/sonar.json", "r") as f:
        sonar = json.load(f)

    coverage = next((m["value"] for m in sonar.get("metrics", []) if m["metric"] == "coverage"), "N/A")
    bugs = next((m["value"] for m in sonar.get("metrics", []) if m["metric"] == "bugs"), "N/A")
    return f"SonarQube Summary:\n- Coverage: {coverage}%\n- Bugs: {bugs}"
