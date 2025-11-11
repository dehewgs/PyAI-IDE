@echo off
REM PyAI IDE Launcher for Windows
REM This script launches the PyAI IDE application with error handling

setlocal enabledelayedexpansion

REM Get the directory where this script is located
cd /d "%~dp0"

REM Display header
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    PyAI IDE Launcher                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from: https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% found
echo.

REM Check if virtual environment exists, if not create it
echo [*] Checking virtual environment...
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create virtual environment
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install/upgrade dependencies
echo [*] Installing dependencies...
pip install -q --upgrade pip
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to upgrade pip
    echo.
    pause
    exit /b 1
)

pip install -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies from requirements.txt
    echo.
    echo Trying to install dependencies individually...
    pip install PyQt5==5.15.9
    pip install PyGithub==2.1.1
    pip install GitPython==3.1.40
    pip install huggingface-hub==0.20.0
    pip install transformers==4.35.0
    pip install torch==2.1.0
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies
        echo Please check your internet connection and try again
        echo.
        pause
        exit /b 1
    )
)
echo [OK] Dependencies installed successfully
echo.

REM Launch the application
echo [*] Launching PyAI IDE...
echo.
python launcher.py %*

REM Check if application exited with error
if errorlevel 1 (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║                    APPLICATION ERROR                           ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo The application exited with an error. Please check the output above.
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo [OK] Application closed successfully
)

REM Deactivate virtual environment on exit
deactivate

endlocal
exit /b 0
