FROM python:3.12-slim-trixie

LABEL org.opencontainers.image.title="simc-web" \
      org.opencontainers.image.description="A lightweight self-hosted web runner for SimulationCraft" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/Bromeego/SimC-Local-Runner"

WORKDIR /app

# Trixie split the client out of docker.io. That package only recommends
# docker-cli, so installing it with --no-install-recommends leaves no docker binary.
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker-cli \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py gunicorn.conf.py ./
COPY templates ./templates
COPY static ./static

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)"

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
