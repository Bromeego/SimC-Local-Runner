FROM python:3.12-slim

LABEL org.opencontainers.image.title="simc-web" \
      org.opencontainers.image.description="A lightweight self-hosted web runner for SimulationCraft" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/Bromeego/SimC-Local-Runner"

WORKDIR /app

RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py gunicorn.conf.py ./
COPY templates ./templates
COPY static ./static

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)"

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
