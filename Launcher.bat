@echo off
REM PyAI IDE Launcher for Windows
REM This script launches the PyAI IDE application

setlocal enabledelayedexpansion

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Launch the application
echo Launching PyAI IDE...
python launcher.py %*

REM Deactivate virtual environment on exit
deactivate

endlocal
