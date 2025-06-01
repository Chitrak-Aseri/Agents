FROM python:3.12-slim AS builder

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install uv
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]