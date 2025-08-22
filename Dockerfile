FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m appuser && chown -R appuser /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x entrypoint.sh

# .env is copied if present in the build context. For sensitive API keys, consider mounting as a volume during runtime, e.g., docker run -v /host/.env:/app/.env

ENV PYTHONUNBUFFERED=1

USER appuser

ENTRYPOINT ["./entrypoint.sh"]