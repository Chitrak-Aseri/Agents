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
    llm = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
    
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


    chain = prompt | llm | parser

    try:
        result = chain.invoke({"content": content, "issues": issues})
        print(result)
        return result.model_dump()
    except Exception as e:
        print("Error parsing reviewer output:", e)
        return {"create_issue": False}

def run_autonomous_issue_agent(data_folder):
    docs = parse_all_documents(data_folder)
    issues = fetch_existing_issues()
    print("************************EXISITING ISSUES*********************************")
    print(issues)
    print("************************EXISITING ISSUES*********************************")
    decision = run_reviewer_agent(docs, issues)
    run_generator_agent(decision)