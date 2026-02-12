@echo off
REM Local Render Deployment Simulator for Windows
REM This script simulates the Render production environment locally

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo.
echo  GG  Local Render Deployment Simulator
echo ============================================================
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo Error: 'backend' directory not found
    echo Run this script from the project root directory
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
cd backend
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed!
cd ..

REM Check gunicorn
echo Checking gunicorn...
python -m pip show gunicorn >nul 2>&1
if errorlevel 1 (
    echo Installing gunicorn...
    python -m pip install gunicorn -q
)

echo.
echo ============================================================
echo Choose deployment mode:
echo ============================================================
echo 1 - Production mode (gunicorn - like Render)
echo 2 - Development mode (Flask dev server)
echo 3 - Exit
echo.

set /p choice="Enter your choice (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Launching backend in PRODUCTION mode with gunicorn...
    echo Configure: http://localhost:5000
    echo API: http://localhost:5000/api
    echo.
    echo Press Ctrl+C to stop
    echo.
    cd backend
    set FLASK_ENV=production
    set FLASK_DEBUG=False
    set PORT=5000
    python -m gunicorn -w 2 -b 0.0.0.0:5000 --worker-class sync wsgi:app
    cd ..
) else if "%choice%"=="2" (
    echo.
    echo Launching backend in DEVELOPMENT mode with Flask...
    echo Configure: http://localhost:5000
    echo API: http://localhost:5000/api
    echo.
    echo Press Ctrl+C to stop
    echo.
    cd backend
    set FLASK_ENV=development
    set FLASK_DEBUG=True
    python -m flask run
    cd ..
) else if "%choice%"=="3" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice
    pause
    exit /b 1
)

endlocal
