# code-review-agent/main.py

import os
import json
import glob
from langchain.output_parsers import RegexParser
from agents.review_agent import ReviewAgent
from core.models import get_model_instance
from utils.config_loader import load_config
from utils.file_loader import load_codebase


def get_file_structure(root, include_paths, exclude_paths):
    exclude_abs = [os.path.abspath(os.path.join(root, p)) for p in exclude_paths]
    result = []
    for path in include_paths:
        abs_path = os.path.abspath(os.path.join(root, path))
        for f in glob.glob(os.path.join(abs_path, "**"), recursive=True):
            abs_file = os.path.abspath(f)
            if os.path.isfile(abs_file) and not any(abs_file.startswith(ex) for ex in exclude_abs):
                result.append(abs_file.replace(root, ""))
    return "\n".join(result)

import json
import re

def parse_llm_response_to_json(response_text: str) -> dict:
    """
    Tries to parse JSON content from the response text.
    Handles:
    - Raw JSON
    - JSON wrapped in triple quotes
    - JSON in ```json fenced blocks
    """
    response_text = response_text.strip()

    # Handle triple quotes edge case
    response_text = response_text.strip('"""').strip("```").strip()

    # Try parsing raw JSON directly
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON using regex as fallback
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
    config = load_config()
    root_dir = os.getcwd()

    includes = config.get("include", [])
    excludes = config.get("exclude", [])

    structure = get_file_structure(root_dir, includes, excludes)

    code_files = load_codebase(
        includes=[os.path.join(root_dir, path) for path in includes],
        excludes=[os.path.join(root_dir, path) for path in excludes]
    )

    if not code_files:
        print("❌ No Python files found for review. Please check include/exclude paths.")
        exit(1)

    code = "\n\n".join([
        f"### {file_path.replace(root_dir, '')} ###\n{content}"
        for file_path, content in code_files
    ])

    model = get_model_instance(config["model"])
    agent = ReviewAgent(model)

    review_result = agent.generate_code_review(code, structure)
    print("\n\nAI REVIEW OUTPUT:\n", review_result)

    try:
        # Persist the structured output
        with open("code_review_result.json", "w") as f:
            json.dump(review_result.dict(), f, indent=4)

        print("✅ Saved parsed review JSON to 'code_review_result.json'")

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
