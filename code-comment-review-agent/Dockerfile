FROM python:3.12-slim AS builder

WORKDIR /code-comment-review-agent

COPY . ./code-comment-review-agent

RUN pip install --upgrade pip
RUN pip install uv
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /code-comment-review-agent/code-comment-review-agent

RUN uv export --no-dev --no-hashes > requirements.txt
RUN pip install -r requirements.txt

# Set the working directory to ensure Python finds the `src` module
ENV PYTHONPATH=/code-comment-review-agent/code-comment-review-agent

ENTRYPOINT ["python", "-m", "code_commenter.main"]
