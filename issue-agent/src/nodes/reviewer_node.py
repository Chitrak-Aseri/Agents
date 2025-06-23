from typing import Any, Dict, List, Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from src.utils.parser import summarize_sonar_metrics


class Issue(BaseModel):
    title: str
    body: str


class ReviewerOutput(BaseModel):
    create_issues: bool
    ISSUES: Optional[List[Issue]] = None


def run_reviewer_agent(state: Dict[str, Any], llm, issues: str) -> Dict[str, Any]:
    parsed_input = state["parsed_input"]
    parser = PydanticOutputParser(pydantic_object=ReviewerOutput)

    llm_text = parsed_input.get("llm_text", "")
    sonar_data = parsed_input.get("sonar", {})
    sonar_summary = summarize_sonar_metrics(sonar_data)

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
6. Avoid vague or generic issues; be specific about the problem and its context.
7. If no new issues are needed, return `create_issues=False` and an empty list for `ISSUES`.
8. If new issues are needed, return `create_issues=True` and list all new issues under the key `ISSUES`.

Given the following documents and metrics:
{content}

And the following current GitHub issues:
{issues}

{format_instructions}
""",
        input_variables=["content", "issues"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    result = chain.invoke({"content": full_content, "issues": issues})

    create_issues = result.create_issues
    issues_to_create = [i.dict() for i in result.ISSUES] if result.ISSUES else []

    return {
        **state,
        "review_result": result,
        "decision": create_issues,
        "issues_to_create": issues_to_create,
    }
