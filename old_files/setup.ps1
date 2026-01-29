# YOLO26 Face Detection Project - Setup Script (PowerShell)
# Run with: .\setup.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "YOLO26 Face Detection Project - Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

# Create virtual environment
Write-Host "[2/4] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists, skipping creation" -ForegroundColor Green
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        pause
        exit 1
    }
}
Write-Host ""

# Activate virtual environment and install requirements
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "⚠ Some dependencies may have failed to install" -ForegroundColor Yellow
}
Write-Host ""

# Create necessary directories
Write-Host "[4/4] Setting up directories..." -ForegroundColor Yellow
@("output", "models", "test") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ | Out-Null
        Write-Host "  Created: $_\" -ForegroundColor Gray
    } else {
        Write-Host "  Exists: $_\" -ForegroundColor Gray
    }
}
Write-Host ""

Write-Host "============================================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the project:" -ForegroundColor Cyan
Write-Host "  1. Activate virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Run main menu: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Or simply run: .\run.ps1" -ForegroundColor Cyan
Write-Host ""
pause
