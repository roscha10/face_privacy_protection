@echo off
echo Starting YOLO26 Face Detection Project...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run main
call venv\Scripts\activate.bat
python main.py

pause
