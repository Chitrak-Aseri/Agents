from langchain_core.tools import tool  # ✅ CORRECT
from github import Github
import os

@tool
def create_issue(input: str) -> str:
    """
    Create a GitHub issue.

    Input format: 'title::Some title|||body::Issue body'
    """
    parts = dict(i.split('::', 1) for i in input.split('|||'))
    title = parts.get("title", "Untitled")
    body = parts.get("body", "No content")
    
    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["GITHUB_REPO"])
    issue = repo.create_issue(title=title, body=body, labels=["issue-agent"])
    return f"Issue created: {issue.html_url}"
