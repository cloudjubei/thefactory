FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# .env is copied if present in the build context. For sensitive API keys, consider mounting as a volume during runtime, e.g., docker run -v /host/.env:/app/.env

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "while true; do python scripts/autonomous_agent.py --agent developer --model gpt-4-turbo-preview; sleep 3600; done"]
