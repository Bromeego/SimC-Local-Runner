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

rem Ask Compose for the published port so a custom SIMC_WEB_PORT is respected.
set "APP_PORT="
for /f "delims=" %%p in ('docker compose port simc-web 8080 2^>nul') do if not defined APP_PORT set "APP_PORT=%%p"
if not defined APP_PORT set "APP_PORT=8088"
:strip_host
if not "%APP_PORT::=%"=="%APP_PORT%" (
    set "APP_PORT=%APP_PORT:*:=%"
    goto strip_host
)
set "APP_URL=http://localhost:%APP_PORT%"

echo.
echo SimC Local Runner is starting at %APP_URL%
start "" "%APP_URL%"
exit /b 0

:failed
echo.
echo SimC Local Runner could not be started. The Docker output above may explain why.
pause
exit /b 1
