from github import Github
import os
from dotenv import load_dotenv
load_dotenv()
gh = Github(os.environ["GITHUB_TOKEN"], seconds_between_writes=1)
repo = gh.get_repo("Manav-Khandurie/fastapi-learning")

issue = repo.get_issue(number=591)
issue.create_comment("🔧 Test comment from token!")
