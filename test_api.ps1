# Example API usage for Job Web Scraper
# Run this script to test all API endpoints

# Make sure the Flask backend is running first:
# python -m backend.app

Write-Host "=== Job Web Scraper API Examples ===" -ForegroundColor Cyan
Write-Host "`nMake sure Flask backend is running (python -m backend.app)`n"

$API_BASE = "http://localhost:5000"

# 1. Health Check
Write-Host "1. Health Check" -ForegroundColor Green
Write-Host "GET /health" -ForegroundColor Gray
$response = Invoke-WebRequest -Uri "$API_BASE/health"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
Write-Host ""

# 2. Scrape Jobs
Write-Host "2. Scrape Jobs from RemoteOK and Himalayas" -ForegroundColor Green
Write-Host "POST /api/scrape (query='python developer')" -ForegroundColor Gray
$body = @{
    query = "python developer"
    sources = @("remoteok", "himalayas")
    pages = 1
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "$API_BASE/api/scrape" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
Write-Host ""

# 3. Get Jobs
Write-Host "3. Get Jobs (first 5)" -ForegroundColor Green
Write-Host "GET /api/jobs" -ForegroundColor Gray
$response = Invoke-WebRequest -Uri "$API_BASE/api/jobs"
$jobs = $response.Content | ConvertFrom-Json
$jobs | Select-Object -First 5 | ConvertTo-Json -Depth 3
Write-Host ""

# 4. Get Analysis
Write-Host "4. Get Analysis" -ForegroundColor Green
Write-Host "GET /api/analysis" -ForegroundColor Gray
$response = Invoke-WebRequest -Uri "$API_BASE/api/analysis"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
Write-Host ""

# 5. Get Simple Summary
Write-Host "5. Get Simple Summary" -ForegroundColor Green
Write-Host "POST /api/summary (use_ai=false)" -ForegroundColor Gray
$body = @{ use_ai = $false } | ConvertTo-Json
$response = Invoke-WebRequest -Uri "$API_BASE/api/summary" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
Write-Host ""

# 6. Get AI Summary (if Gemini key is set)
Write-Host "6. Get AI Summary (Gemini)" -ForegroundColor Green
Write-Host "POST /api/summary (use_ai=true)" -ForegroundColor Gray
$body = @{
    use_ai = $true
    prompt = "Focus on top 5 skills for AI/ML roles in 2025"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$API_BASE/api/summary" -Method POST -Body $body -ContentType "application/json"
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Note: Gemini API not configured or unreachable. Set GEMINI_API_KEY env var." -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Gray
}

Write-Host "`n=== All tests complete ===" -ForegroundColor Cyan
