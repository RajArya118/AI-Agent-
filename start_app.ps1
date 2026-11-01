Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting AI Personal Assistant Web Application" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path "$scriptDir\backend"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Python virtual environment not found. Setting up..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}

Write-Host "`nStarting AI Assistant full-stack server..." -ForegroundColor Green
Write-Host "Opening web browser at http://localhost:8000" -ForegroundColor Green
Start-Process "http://localhost:8000"

.\.venv\Scripts\python.exe run.py
