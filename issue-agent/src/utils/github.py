import os

from dotenv import load_dotenv
from github import Github

load_dotenv()


def fetch_existing_issues():
    """Fetch all open issues from a GitHub repository.

    Returns:
        list: A list of strings containing issue titles and bodies in the format "title: body".
              Each string represents one open issue from the specified repository.

    Note:
        Requires GITHUB_TOKEN and GITHUB_REPO environment variables to be set,
        typically through a .env file loaded by dotenv.
    """
    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["GITHUB_REPO"])
    # Get all open issues and format them as "title: body" strings
    return [f"{i.title}: {i.body}" for i in repo.get_issues(state="open")]
