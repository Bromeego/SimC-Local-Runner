@echo off
setlocal
cd /d "%~dp0"

where docker >nul 2>&1
if errorlevel 1 (
    echo Docker was not found. Install Docker Desktop, then try again.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Start Docker Desktop, then try again.
    pause
    exit /b 1
)

echo Updating SimC Local Runner...
docker compose pull simc-web
if errorlevel 1 echo The update check failed. Trying the locally cached image instead.

echo Starting SimC Local Runner...
docker compose up -d --wait --wait-timeout 90
if errorlevel 1 goto failed

echo.
echo SimC Local Runner is starting at http://localhost:8088
start "" "http://localhost:8088"
exit /b 0

:failed
echo.
echo SimC Local Runner could not be started. The Docker output above may explain why.
pause
exit /b 1
