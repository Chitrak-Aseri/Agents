from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Optional, List


class Issue(BaseModel):
    title: str
    body: str


class ReviewerOutput(BaseModel):
    create_issues: bool
    ISSUES: Optional[List[Issue]] = None


def summarize_sonar_metrics(sonar: dict) -> str:
    """Extract key insights from structured sonar report for reviewer prompt."""
    if not sonar:
        return ""

    summary = []

    # Quality Gate
    gate = sonar.get("quality_gate", {})
    status = gate.get("status", "UNKNOWN")
    conditions = gate.get("conditions", [])
    summary.append(f"Quality Gate Status: **{status}**")
    for cond in conditions:
        summary.append(
            f"- {cond.get('metricKey')}: {cond.get('actual')} "
            f"(threshold: {cond.get('errorThreshold')}) => {cond.get('status')}"
        )

    # Metrics
    metric_map = {m["metric"]: m["value"] for m in sonar.get("metrics", []) if "value" in m}
    coverage = metric_map.get("coverage")
    complexity = metric_map.get("complexity")
    bugs = metric_map.get("bugs")
    vulnerabilities = metric_map.get("vulnerabilities")

    if coverage:
        summary.append(f"- Coverage: {coverage}%")
    if complexity:
        summary.append(f"- Complexity: {complexity}")
    if bugs:
        summary.append(f"- Bugs: {bugs}")
    if vulnerabilities:
        summary.append(f"- Vulnerabilities: {vulnerabilities}")

    return "\n".join(summary)


def run_reviewer_agent(*, parsed_input: dict, issues: str, llms: list):
    """
    parsed_input: dict with keys:
        - llm_text: combined document text
        - sonar: structured sonar report (dict)
    issues: current GitHub issues (str)
    llms: list of LLM objects
    """

    parser = PydanticOutputParser(pydantic_object=ReviewerOutput)

    # Extract parts from parsed input
    llm_text = parsed_input.get("llm_text", "")
    sonar_data = parsed_input.get("sonar", {})
    sonar_summary = summarize_sonar_metrics(sonar_data)

    # Compose full content
    full_content = f"{llm_text}\n\n### SonarQube Metrics Summary:\n{sonar_summary}"

    prompt = PromptTemplate(
        template="""
You are an autonomous reviewer AI designed to assist in managing GitHub issues effectively.
Your objective is to analyze the provided documents and the list of currently open GitHub issues to determine whether any **new and non-redundant** issues should be created.

### Instructions:

1. Carefully compare the documents and SonarQube metrics against the current issues.
2. Identify **gaps, untracked problems, or opportunities for improvement** that are **not already covered** by any existing issue.
3. Avoid creating duplicate or overlapping issues — each suggested issue must represent a **unique and clearly distinct concern**.
4. Group similar observations under a single cohesive issue where applicable to reduce noise.
5. Ensure each new issue has a **concise, descriptive title** and a **clear, actionable description**.

Given the following documents and metrics:
{content}

And the following current GitHub issues:
{issues}

Decide whether new GitHub issues should be created.

If yes, return create_issues=True and list all new issues under the key ISSUES.

{format_instructions}
""",
        input_variables=["content", "issues"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    best_result = {"create_issues": False, "ISSUES": []}
    max_issues = 0

    for llm in llms:
        print(f"\n🔍 Running reviewer with model: {llm.__class__.__name__}")
        chain = prompt | llm | parser
        try:
            result = chain.invoke({
                "content": full_content,
                "issues": issues
            })
            issue_count = len(result.ISSUES) if result.ISSUES else 0

            if issue_count > max_issues:
                best_result = result.model_dump()
                max_issues = issue_count

            print(f"✅ Model {llm.__class__.__name__} returned {issue_count} issue(s).")

        except Exception as e:
            print(f"❌ Error from model {llm.__class__.__name__}:", e)

    return best_result
