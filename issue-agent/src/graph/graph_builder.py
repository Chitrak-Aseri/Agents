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
        You are an autonomous reviewer AI.

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
    decision = run_reviewer_agent(docs, issues)
    run_generator_agent(decision)