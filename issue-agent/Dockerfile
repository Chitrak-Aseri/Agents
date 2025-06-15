FROM python:3.12-slim AS builder

WORKDIR /issue-agent

COPY . ./issue-agent

RUN pip install --upgrade pip
RUN pip install uv
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /issue-agent/issue-agent

RUN uv export --no-dev --no-hashes > requirements.txt
RUN pip install -r requirements.txt

# Set the working directory to ensure Python finds the `src` module
ENV PYTHONPATH=/issue-agent/issue-agent

ENTRYPOINT ["python", "-m", "src.main"]
