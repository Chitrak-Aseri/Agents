# code-review-agent/utils/file_loader.py
import os

def load_codebase(includes, excludes=None, max_file_size_kb=1000000000):
    excludes = excludes or []
    excludes_abs = [os.path.abspath(ex) for ex in excludes]
    print(excludes_abs)
    code_files = []
    for include_path in includes:
        include_abs = os.path.abspath(include_path)
        for root, dirs, files in os.walk(include_abs):
            root_abs = os.path.abspath(root)

            if any(root_abs.startswith(ex) for ex in excludes_abs):
                continue

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root_abs, file)
                    if any(full_path.startswith(ex) for ex in excludes_abs):
                        continue
                    if os.path.getsize(full_path) <= max_file_size_kb * 1024:
                        with open(full_path, "r") as f:
                            code_files.append((full_path, f.read()))
    return code_files
