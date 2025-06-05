FROM python:3.12-slim AS builder

COPY . .

RUN pip install --upgrade pip
RUN pip install uv
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN uv export --no-dev --no-hashes > requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "src.main"]
