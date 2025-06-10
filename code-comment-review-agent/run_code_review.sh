#!/bin/bash
set -e

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <API_URL> <CONFIG_FILE>"
  exit 1
fi

API_URL=$1
CONFIG_FILE=$2

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python3 required but not found. Aborting."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo >&2 "jq required but not found. Aborting."; exit 1; }
command -v tree >/dev/null 2>&1 || { echo >&2 "tree required but not found. Aborting."; exit 1; }

# Parse config values
PROVIDER=$(python3 -c "
import yaml, json
with open('$CONFIG_FILE', 'r') as f:
    y = yaml.safe_load(f)
print(json.dumps(y.get('model', {}).get('provider', {})))
")

MODEL_NAME=$(python3 -c "
import yaml
with open('$CONFIG_FILE', 'r') as f:
    y = yaml.safe_load(f)
print(y.get('model', {}).get('model_name', 'gpt-4o'))
")

INCLUDE_DIRS=$(python3 -c "
import yaml, json
with open('$CONFIG_FILE', 'r') as f:
    y = yaml.safe_load(f)
print(json.dumps(y.get('include', [])))
")

EXCLUDE_PATTERNS=$(python3 -c "
import yaml, json
with open('$CONFIG_FILE', 'r') as f:
    y = yaml.safe_load(f)
print(json.dumps(y.get('exclude', [])))
")

# Collect code content from included dirs
CODE_CONTENT=$(python3 -c "
import os, json, fnmatch

include = json.loads('$INCLUDE_DIRS')
exclude = json.loads('$EXCLUDE_PATTERNS')

def is_excluded(path):
    for pattern in exclude:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

code_files = []
for inc in include:
    for root, _, files in os.walk(inc):
        if is_excluded(root):
            continue
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path)
            if f.endswith('.py') and not is_excluded(rel_path):
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                code_files.append(f'### {rel_path} ###\\n' + content)

print(json.dumps('\\n\n'.join(code_files)))
")

# Get file structure (as a stringified JSON)
FILE_STRUCT=$(tree -a -J $(echo "$INCLUDE_DIRS" | jq -r '.[]') | jq -c '.')

# Compose final payload
PAYLOAD=$(jq -n \
  --argjson provider "$PROVIDER" \
  --arg model_name "$MODEL_NAME" \
  --arg code "$CODE_CONTENT" \
  --arg file_struct "$FILE_STRUCT" \
  '{provider: $provider, model_name: $model_name, code: $code, file_struct: $file_struct}')

# POST to FastAPI server
curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" -o code_review_result.json

echo "✅ Code review results saved to code_review_result.json"
