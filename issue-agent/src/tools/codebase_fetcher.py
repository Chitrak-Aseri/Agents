import os
from langchain_core.tools import tool


def generate_tree_structure(directory: str, prefix: str = '') -> str:
    """Generates a text-based tree structure of a directory."""
    entries = sorted(os.listdir(directory))
    lines = []

    for idx, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        connector = '└── ' if idx == len(entries) - 1 else '├── '
        lines.append(f"{prefix}{connector}{entry}")
        if os.path.isdir(path):
            extension = '    ' if idx == len(entries) - 1 else '│   '
            lines.extend(generate_tree_structure(path, prefix + extension))

    return '\n'.join(lines)


def read_codebase_files(directory: str) -> str:
    """Reads all text-based files in the directory recursively and returns a structured string."""
    file_contents = []

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    rel_path = os.path.relpath(filepath, directory)
                    file_contents.append(f"\n### {rel_path}\n\n```\n{content}\n```")
            except Exception as e:
                file_contents.append(f"\n### {rel_path} (could not read): {e}")

    return "\n".join(file_contents)

@tool
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



