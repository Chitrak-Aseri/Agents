FROM python:3.12-slim

LABEL maintainer="Manav Khandurie <manavkhandurie@gmail.com>"

# Safe directory for bot
WORKDIR /opt/bot

# Install system deps
RUN apt-get update && apt-get install -y git curl && apt-get clean

# Poetry setup
COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip
RUN pip install poetry poetry-plugin-export
RUN poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt

# Copy your full bot source here (not in /github/workspace!)
COPY . .

# Set PYTHONPATH to your own codebase
ENV PYTHONPATH=/opt/bot

# Run the entrypoint — which now executes within your own codebase
ENTRYPOINT ["python", "/opt/bot/entrypoint.py"]
