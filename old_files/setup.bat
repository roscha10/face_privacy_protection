@echo off
echo ============================================================
echo YOLO26 Face Detection Project - Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found!
python --version
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment and install requirements
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create necessary directories
echo [4/4] Setting up directories...
if not exist output mkdir output
if not exist models mkdir models
if not exist test mkdir test
echo.

echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo To run the project:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run main menu: python main.py
echo.
echo Or simply run: run.bat
echo.
pause
