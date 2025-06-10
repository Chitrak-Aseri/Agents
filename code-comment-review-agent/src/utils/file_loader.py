# utils/file_loader.py
import os
import fnmatch

def matches_exclude(path, exclude_patterns):
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def load_codebase(root_path, include_paths, exclude_paths):
    from pathlib import Path
    import os

    code_files = []
    exclude_abs = [os.path.abspath(os.path.join(root_path, p)) for p in exclude_paths]

    for rel_path in include_paths:
        abs_path = os.path.abspath(os.path.join(root_path, rel_path))
        if os.path.isdir(abs_path):
            for filepath in Path(abs_path).rglob("*.py"):
                filepath = str(filepath)
                if not any(filepath.startswith(ex) for ex in exclude_abs):
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        code_files.append({
                            "path": filepath.replace(root_path + os.sep, ""),
                            "content": f.read()
                        })
        elif os.path.isfile(abs_path) and abs_path.endswith(".py"):
            if not any(abs_path.startswith(ex) for ex in exclude_abs):
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    code_files.append({
                        "path": abs_path.replace(root_path + os.sep, ""),
                        "content": f.read()
                    })
    return code_files

