# utils/file_loader.py
import os
import fnmatch

def matches_exclude(path, exclude_patterns):
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def load_codebase(includes, excludes=None, max_file_size_kb=1000000000):
    excludes = excludes or []
    code_files = []
    
    exclude_patterns = [os.path.normpath(ex) for ex in excludes]

    for include_path in includes:
        include_abs = os.path.abspath(include_path)
        for root, dirs, files in os.walk(include_abs):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    norm_path = os.path.normpath(full_path)

                    if matches_exclude(norm_path, exclude_patterns):
                        continue

                    if os.path.getsize(full_path) <= max_file_size_kb * 1024:
                        with open(full_path, "r") as f:
                            code_files.append((full_path, f.read()))

    return code_files
