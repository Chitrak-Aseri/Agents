import os
import json
import xmltodict
import time


def parse_sonar_report(report_dir: str = "sonar-report") -> dict:
    """Parses SonarQube report files and returns a merged structured output."""

    def load_json(filename):
        path = os.path.join(report_dir, filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    issues_data = load_json("issues.json")
    quality_gate_data = load_json("quality_gate.json")
    measures_data = load_json("measures.json")

    return {
        "timestamp": int(time.time()),
        "issues": issues_data.get("issues", []),
        "quality_gate": quality_gate_data.get("projectStatus", {}),
        "metrics": measures_data.get("component", {}).get("measures", [])
    } 


def parse_sonar_json(file_path: str) -> dict:
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


def parse_all_documents(folder_path):
    combined_content = ""
    sonar_data = {}

    # Parse SonarQube report folder if exists
    sonar_report_path = os.path.join(folder_path, "sonar-report")
    if os.path.exists(sonar_report_path):
        try:
            structured = parse_sonar_report(sonar_report_path)
            sonar_data = structured  # set sonar_data for output
            combined_content += "\n\n### 📊 SonarQube Summary:\n"
            combined_content += json.dumps(structured, indent=2)
        except Exception as e:
            combined_content += f"\n\n### SonarQube Summary Error: {e}\n"

    # Parse individual files
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file == "sonar.json":
            sonar_parsed = parse_sonar_json(path)
            sonar_data = sonar_parsed["data"]  # override sonar data
            combined_content += "\n\n### SonarQube Issues:\n" + sonar_parsed["text"]

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

    return {
        "llm_text": combined_content.strip(),
        "sonar": sonar_data
    }
