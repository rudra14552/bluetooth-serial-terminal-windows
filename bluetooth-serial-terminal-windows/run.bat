@echo off
echo Bluetooth Serial Terminal
echo ========================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Installing dependencies...
pip install pyserial >nul 2>nul

echo.
echo Starting Bluetooth Serial Terminal...
echo.
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred while running the application.
    pause
)
