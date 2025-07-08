import os
import subprocess
from github import Github

def pr_exists(g, repo_name, branch):
    repo = g.get_repo(repo_name)
    pulls = repo.get_pulls(state="open", head=f"{repo.owner.login}:{branch}")
    return pulls.totalCount > 0

def run():
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", os.getcwd()], check=True)

    # GitHub-related ENV vars
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
    BOT_NAME = os.environ.get("BOT_NAME", "code-comment-bot")
    BOT_EMAIL = os.environ.get("BOT_EMAIL", "bot@your-org.com")
    BRANCH_NAME = os.environ.get("BOT_BRANCH", "auto/comment-update")
    PR_TITLE = os.environ.get("PR_TITLE", "🤖 Add Code Comments")
    PR_BODY = os.environ.get("PR_BODY", "This PR includes auto-generated code comments.")

    # Optional CLI arguments via ENV
    args = ["python", "-m", "bot.cli"]

    def append_flag(name, value):
        if value:
            args.extend([f"--{name}", value])

    append_flag("config", os.environ.get("CONFIG"))
    # Properly handle multiple src paths (split on space)
    src_paths = os.environ.get("SRC", ".").split()
    if src_paths:
        args.append("--src")
        args.extend(src_paths)

    append_flag("provider", os.environ.get("PROVIDER"))
    append_flag("model_name", os.environ.get("MODEL_NAME"))
    append_flag("region", os.environ.get("REGION"))
    append_flag("api_key", os.environ.get("API_KEY"))
    append_flag("api_base", os.environ.get("API_BASE"))
    append_flag("aws_access_key_id", os.environ.get("AWS_ACCESS_KEY_ID"))
    append_flag("aws_secret_access_key", os.environ.get("AWS_SECRET_ACCESS_KEY"))

    # Initialize GitHub client
    gh = Github(GITHUB_TOKEN)
    if pr_exists(gh, GITHUB_REPOSITORY, BRANCH_NAME):
        print("✅ PR already exists. Skipping PR creation.")
        return

    subprocess.run(["git", "config", "user.name", BOT_NAME], check=True)
    subprocess.run(["git", "config", "user.email", BOT_EMAIL], check=True)

    # Run bot CLI
    print("🚀 Running CLI:", " ".join(args))
    subprocess.run(args, check=True)
    print("✅ Done Executing CLI:", " ".join(args))

    # Create/reset branch and stage changes
    subprocess.run(["git", "checkout", "-B", BRANCH_NAME], check=True)
    subprocess.run(["git", "add", "-A"], check=True)

    # Check if any changes are staged
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)

    if status.stdout.strip():
        subprocess.run(["git", "commit", "-m", "🤖 Auto-commented code"], check=True)

        # Push changes
        token_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPOSITORY}.git"
        subprocess.run(["git", "push", token_url, f"{BRANCH_NAME}:{BRANCH_NAME}", "--force"], check=True)

        # Create pull request
        repo = gh.get_repo(GITHUB_REPOSITORY)
        pr = repo.create_pull(title=PR_TITLE, body=PR_BODY, head=BRANCH_NAME, base="main")
        print(f"✅ Pull request created: {pr.html_url}")
    else:
        print("⚠️ No changes detected. Skipping commit, push, and PR creation.")

if __name__ == "__main__":
    run()
