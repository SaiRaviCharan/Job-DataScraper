# Helper script to run the React frontend
# Usage: .\run_frontend.ps1

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Cyan
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Node.js not found. Please install Node.js 14+" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Node.js found" -ForegroundColor Green

# Navigate to frontend folder
cd frontend

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

# Start the dev server
Write-Host "`n✓ Starting React dev server on http://localhost:3000..." -ForegroundColor Green
Write-Host "Make sure the Flask backend is running on http://localhost:5000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop.`n" -ForegroundColor Cyan

npm start
