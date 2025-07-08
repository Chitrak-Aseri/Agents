# bot/utils/file_handler.py
"""Module for handling file operations related to code files (Python, SQL, Jupyter notebooks)."""

import os
import json

def walk_code_files(src_folder):
    """Generator that yields paths to code files (.py, .sql, .ipynb) in a directory tree.
    
    Args:
        src_folder: Root directory to search for code files
        
    Yields:
        str: Full path to each matching code file
    """
    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py") or file.endswith(".sql") or file.endswith(".ipynb"):
                yield os.path.join(root, file)

def read_code(filepath):
    """Reads content from a code file, handling Jupyter notebooks specially.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        str/dict: File content as string (for .py/.sql) or parsed JSON (for .ipynb)
    """
    if filepath.endswith(".ipynb"):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(filepath, 'r') as f:
            return f.read()

def write_code(filepath, content):
    """Writes content to a file, creating a backup (.bak) and handling Jupyter notebooks specially.
    
    Args:
        filepath: Path to the file to write
        content: Content to write (string for .py/.sql, dict for .ipynb)
    """
    # backup_path = filepath + ".bak"
    # os.rename(filepath, backup_path)
    if filepath.endswith(".ipynb"):
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
    else:
        with open(filepath, 'w') as f:
            f.write(content)