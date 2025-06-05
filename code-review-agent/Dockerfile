FROM python:3.12-slim AS builder

# Set working directory to where src/ actually is
WORKDIR /code-review-agent/code-review-agent

COPY . .

RUN pip install --upgrade pip
RUN pip install uv
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN uv export --no-dev --no-hashes > requirements.txt
RUN pip install -r requirements.txt

# Set working directory for runtime as well
WORKDIR /code-review-agent/code-review-agent

ENTRYPOINT ["python", "-m", "src.main"]
