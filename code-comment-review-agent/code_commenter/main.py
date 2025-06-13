# code-review-agent/main.py

import os
import json
import glob
import argparse
from code_commenter.agents.review_comment_agent import ReviewAgent
from code_commenter.core.models import get_model_instance
from code_commenter.utils.config_loader import load_config
from code_commenter.utils.file_loader import load_codebase
import re


def get_file_structure(root, include_paths, exclude_paths):
    """Get the file structure of the codebase as a string.
    
    Args:
        root: Root directory path
        include_paths: List of paths to include
        exclude_paths: List of paths to exclude
        
    Returns:
        str: Newline-separated string of relative file paths
    """
    exclude_abs = [os.path.abspath(os.path.join(root, p)) for p in exclude_paths]
    result = []
    for path in include_paths:
        abs_path = os.path.abspath(os.path.join(root, path))
        for f in glob.glob(os.path.join(abs_path, "**"), recursive=True):
            abs_file = os.path.abspath(f)
            if os.path.isfile(abs_file) and not any(abs_file.startswith(ex) for ex in exclude_abs):
                result.append(abs_file.replace(root, ""))
    return "\n".join(result)


def parse_llm_response_to_json(response_text: str) -> dict:
    """Parse LLM response text to extract JSON content.
    
    Args:
        response_text: Raw response text from LLM
        
    Returns:
        dict: Parsed JSON content
        
    Raises:
        ValueError: If no valid JSON could be extracted
    """
    response_text = response_text.strip()
    response_text = response_text.strip('"""').strip("```").strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    json_regex = r"\{[\s\S]*?\}"
    match = re.search(json_regex, response_text)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Regex found JSON but failed to parse: {e}")

    raise ValueError("Failed to extract JSON from the LLM response.")


def main():
    """Main entry point for the code review CLI tool."""
    parser = argparse.ArgumentParser(description="AI Code Reviewer CLI")

    parser.add_argument(
        "--config",
        type=str,
        default="ai-comment-reviewer.yaml",
        help="Path to the config YAML file (default: ai-comment-reviewer.yaml)"
    )

    parser.add_argument(
        "--score-threshold",
        type=int,
        help="Override the score threshold defined in the config"
    )
    args = parser.parse_args()
    config_path = os.path.abspath(args.config)

    # Load config with overrides
    config = load_config(path=args.config, overrides={
        "score_threshold": args.score_threshold
    })

    # 👇 Use the config file location to infer the repo root
    root_dir = os.path.abspath(os.getcwd())
    includes = config.get("include", [])
    excludes = config.get("exclude", [])

    structure = get_file_structure(root_dir, includes, excludes)

    code_files = load_codebase(
        root_path=root_dir,
        include_paths=includes,
        exclude_paths=excludes
    )
    if not code_files:
        print("-------------------------ROOTDIR-------------------")
        print(root_dir)
        print("-------------------------ROOTDIR-------------------")
        print("-------------------------INCLUDES-------------------")
        print(includes)
        print("-------------------------INCLUDES-------------------")
        print("-------------------------EXCLUDES-------------------")
        print(excludes)
        print("-------------------------EXCLUDES-------------------")
        print("❌ No Python files found for review. Please check include/exclude paths.")
        exit(1)

    for file in code_files:
        print(" -", file["path"])

    code = "\n\n".join([
        f"### {file['path']} ###\n{file['content']}"
        for file in code_files
    ])

    model = get_model_instance(config["model"])
    agent = ReviewAgent(model)
    review_result = agent.generate_code_review(code, structure)

    print("\n\nAI REVIEW OUTPUT:\n", review_result)

    try:
        with open("code_comment_review_result.json", "w") as f:
            json.dump(review_result.dict(), f, indent=4)

        print("✅ Saved parsed review JSON to 'code_comment_review_result.json'")

        score = review_result.score
        threshold = config.get("score_threshold", 70)

        if score < threshold:
            print(f"\n❌ Score below threshold ({score} < {threshold})")
            exit(1)
        else:
            print(f"\n✅ Score passed ({score} >= {threshold})")
            exit(0)

    except Exception as e:
        print("❌ Error parsing response:", e)
        exit(1)


if __name__ == "__main__":
    main()