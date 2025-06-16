from github import Github
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_existing_issues():
    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["GITHUB_REPO"])
    return [f"{i.title}: {i.body}" for i in repo.get_issues(state="open")]