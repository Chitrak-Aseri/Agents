from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional,List
import os
import json
from src.utils.parser import parse_all_documents
from src.utils.github import fetch_existing_issues
from src.agents.generator_agent import run_generator_agent
from src.core.models import ModelFactory
from src.utils.config_loader import load_config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
import re

class Issue(BaseModel):
    title: str
    body: str


class ReviewerOutput(BaseModel):
    create_issues: bool
    ISSUES: Optional[List[Issue]] = None

def run_reviewer_agent(content, issues):

    config = load_config()
    factory = ModelFactory(config)
    llms = factory.get_llms()
    
    parser = PydanticOutputParser(pydantic_object=ReviewerOutput)

    prompt = PromptTemplate(
        template="""
        You are an autonomous reviewer AI designed to assist in managing GitHub issues effectively.
        Your objective is to analyze the provided documents and the list of currently open GitHub issues to determine whether any **new and non-redundant** issues should be created.

        ### Instructions:

        1. Carefully compare the documents against the current issues.
        2. Identify **gaps, untracked problems, or opportunities for improvement** that are **not already covered** by any existing issue.
        3. Avoid creating duplicate or overlapping issues — each suggested issue must represent a **unique and clearly distinct concern**.
        4. Group similar observations under a single cohesive issue where applicable to reduce noise.
        5. Ensure each new issue has a **concise, descriptive title** and a **clear, actionable description**.

        Given the following documents:
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
            result = chain.invoke({"content": content, "issues": issues})
            issue_count = len(result.ISSUES) if result.ISSUES else 0

            if issue_count > max_issues:
                best_result = result.model_dump()
                max_issues = issue_count

            print(f"✅ Model {llm.__class__.__name__} returned {issue_count} issue(s).")

        except Exception as e:
            print(f"❌ Error from model {llm.__class__.__name__}:", e)

    return best_result




def run_autonomous_issue_agent(data_folder):
    docs = parse_all_documents(data_folder)
    issues = fetch_existing_issues()
    print("************************EXISITING ISSUES*********************************")
    print(issues)
    print("************************EXISITING ISSUES*********************************")
    decision = run_reviewer_agent(docs, issues)
    run_generator_agent(decision)