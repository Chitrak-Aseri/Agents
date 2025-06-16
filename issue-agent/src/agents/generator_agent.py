from github import Github
import os


def run_generator_agent(data):
    print("****************DATA*******************************")
    print(data)
    print("****************DATA*******************************")

    if not data.get("create_issues"):
        print("No new issues needed.")
        return

    issues = data.get("ISSUES", [])
    if not issues:
        print("No issue details found.")
        return

    gh = Github(os.environ["GITHUB_TOKEN"])
    repo = gh.get_repo(os.environ["GITHUB_REPO"])

    if not repo.has_issues:
        print("🚫 Issues are disabled for this repository.")
        return

    for issue in issues:
        title = issue.get("title")
        body = issue.get("body")
        if title and body:
            repo.create_issue(title=title, body=body)
            print(f"✅ Created issue: {title}")
