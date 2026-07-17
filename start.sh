#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "Docker was not found. Install and start Docker Desktop, then try again."
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Start Docker Desktop or Docker Engine, then try again."
    exit 1
fi

echo "Updating SimC Local Runner..."
if ! docker compose pull simc-web; then
    echo "The update check failed. Trying the locally cached image instead."
fi

echo "Starting SimC Local Runner..."
docker compose up -d --wait --wait-timeout 90

APP_URL="http://localhost:8088"
echo ""
echo "SimC Local Runner is starting at $APP_URL"

case "$(uname -s)" in
    Darwin)
        open "$APP_URL" >/dev/null 2>&1 || true
        ;;
    Linux)
        if [ -n "${DISPLAY:-}" ] && command -v xdg-open >/dev/null 2>&1; then
            xdg-open "$APP_URL" >/dev/null 2>&1 || true
        fi
        ;;
esac
