from langchain_core.tools import tool  # ✅ CORRECT
from github import Github
import os

@tool
def fetch_github_issues() -> str:
    """Fetch all open GitHub issues as a plain text list."""
    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["GITHUB_REPO"])
    return "\n".join(f"- {issue.title}" for issue in repo.get_issues(state="open"))
