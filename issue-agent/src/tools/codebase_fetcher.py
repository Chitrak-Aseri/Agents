import os
import re
# from langchain_core.tools import tool


def extract_file_path_from_body(body: str) -> str:
    match = re.search(r"(src/\S+\.py)", body)
    return match.group(1) if match else ""
# Add this new function
def get_codebase_as_dict(directory: str = "codebase") -> dict:
    """Returns a dictionary of relative file paths to their code content."""
    code_dict = {}

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    rel_path = os.path.relpath(filepath, directory)
                    code_dict[rel_path] = content
            except Exception as e:
                code_dict[rel_path] = f"Could not read file: {e}"

    return code_dict


def generate_tree_structure(directory: str, prefix: str = "") -> str:
    """Generates a text-based tree structure of a directory."""
    entries = sorted(os.listdir(directory))
    lines = []

    for idx, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        connector = "└── " if idx == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{entry}")
        if os.path.isdir(path):
            extension = "    " if idx == len(entries) - 1 else "│   "
            lines.extend(generate_tree_structure(path, prefix + extension))

    return "\n".join(lines)


def read_codebase_files(directory: str) -> str:
    """Reads all text-based files in the directory recursively and returns a structured string."""
    file_contents = []

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if not file.endswith((".py")):
                continue
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    rel_path = os.path.relpath(filepath, directory)
                    file_contents.append(f"\n### {rel_path}\n\n```\n{content}\n```")
            except Exception as e:
                file_contents.append(f"\n### {rel_path} (could not read): {e}")

    return "\n".join(file_contents)


# @tool
def fetch_codebase(directory: str = "codebase") -> str:
    """Combines tree structure and file contents into a single large string."""
    tree = generate_tree_structure(directory)
    code = read_codebase_files(directory)

    return f"""
        ### DIRECTORY STRUCTURE:
        {tree}

        ### CODEBASE:

        {code}
        """


if __name__ == "__main__":
    directory = "codebase"

    # 1. Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"❌ ERROR: Directory '{directory}' not found. Check your path.")
        exit(1)

    # 2. Run the dict fetcher
    codebase = get_codebase_as_dict(directory)
    print("✅ Codebase files loaded:")
    for k, v in codebase.items():
        print(f"📄 {k} → {len(v)} chars")

    # 3. Test path extraction
    test_text = "Please check src/main.py for the main logic."
    extracted = extract_file_path_from_body(test_text)
    print(f"\n🧠 Extracted file path: {extracted}")

    # 4. Run the tree structure generator
    tree_structure = generate_tree_structure(directory)
    print("\n📂 Directory Tree Structure:")
