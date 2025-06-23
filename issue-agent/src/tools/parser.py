import json
import os
import time

import xmltodict
from langchain_core.tools import tool


def parse_sonar_json(file_path: str) -> dict:
    """Parse SonarQube JSON report file into structured data.

    Args:
        file_path: Path to sonar.json file

    Returns:
        Dictionary containing:
        - 'text': Formatted issue details (or error message if no issues)
        - 'data': Raw parsed JSON data
    """
    if not os.path.exists(file_path):
        return {"text": "No sonar.json found.", "data": {}}

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = data.get("issues", [])
    if not issues:
        return {"text": "No issues found in sonar.json.", "data": data}

    formatted_issues = []
    for issue in issues:
        formatted_issues.append(
            f"- Rule: {issue.get('ruleId')}\n"
            f"  Severity: {issue.get('severity')}\n"
            f"  Type: {issue.get('type')}\n"
            f"  Message: {issue.get('message')}\n"
            f"  File: {issue.get('file')}:{issue.get('line')}"
        )

    return {"text": "\n\n".join(formatted_issues), "data": data}


@tool
def parse_all_documents(folder_path: str = "data") -> dict:
    """Parse all documents in a folder and combine their contents.

    Args:
        folder_path: Path to directory containing various report files

    Returns:
        Dictionary containing:
        - 'llm_text': Combined content of all parsed files
        - 'sonar': Parsed SonarQube data (if sonar.json exists)
    """
    combined_content = ""
    # Parse individual files
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file == "sonar.json":
            sonar_parsed = parse_sonar_json(path)
            sonar_data = sonar_parsed["data"]  # override sonar data
            combined_content += "\n\n### SonarQube Issues:\n" + sonar_parsed["text"]
            # print(
            #     "****************************SONAR REPORT************************************"
            # )
            # print("Parsed sonar.json successfully.")
            # print(
            #     "Sonar data:", str(sonar_data)[:1000]
            # )  # Print only the first 1000 characters for brevity
            # print(
            #     "****************************SONAR REPORT************************************"
            # )

        elif file.endswith(".xml"):
            with open(path, "r", encoding="utf-8") as f:
                doc = xmltodict.parse(f.read())
                combined_content += "\n\n### XML Content:\n" + json.dumps(doc, indent=2)

        elif file.endswith(".json") and file != "sonar.json":
            with open(path, "r", encoding="utf-8") as f:
                combined_content += "\n\n### JSON Content:\n" + f.read()

        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                combined_content += "\n\n### Text Content:\n" + f.read()

    return {"llm_text": combined_content.strip(), "sonar": sonar_data}
