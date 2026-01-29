# YOLO26 Face Detection Project - Run Script (PowerShell)
# Run with: .\run.ps1

Write-Host "Starting YOLO26 Face Detection Project..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run: .\setup.ps1" -ForegroundColor White
    pause
    exit 1
}

# Activate virtual environment and run main
& "venv\Scripts\Activate.ps1"
python main.py

pause
