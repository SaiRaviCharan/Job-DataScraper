# Helper script to run the Job Web Scraper backend
# Usage: .\run_backend.ps1

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Cyan
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python found" -ForegroundColor Green

# Check if venv exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install/upgrade requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env from example if not exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠ Please edit .env and add your GEMINI_API_KEY if you want AI summaries" -ForegroundColor Yellow
}

# Run the Flask app
Write-Host "`n✓ Setup complete. Starting Flask backend on http://localhost:5000..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop.`n" -ForegroundColor Cyan

python -m backend.app
