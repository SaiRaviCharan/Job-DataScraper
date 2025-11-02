# Helper script to initialize git and push to GitHub
# Usage: .\init_and_push_github.ps1

Write-Host "=== Jobscraper: Initialize Git & Push to GitHub ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git not found. Please install Git from https://git-scm.com" -ForegroundColor Red
    exit 1
}

# Check if already a git repo
if (Test-Path ".git") {
    Write-Host "[INFO] Git repository already initialized" -ForegroundColor Yellow
}
else {
    Write-Host "[SETUP] Initializing git repository..." -ForegroundColor Green
    git init
    git config user.email "your@email.com"
    git config user.name "Your Name"
}

# Ask for GitHub URL
Write-Host ""
Write-Host "[PROMPT] Enter your GitHub repository URL" -ForegroundColor Cyan
Write-Host "   Example: https://github.com/yourusername/jobscraper.git" -ForegroundColor Gray
$githubUrl = Read-Host "GitHub URL"

if ([string]::IsNullOrWhiteSpace($githubUrl)) {
    Write-Host "[ERROR] GitHub URL cannot be empty" -ForegroundColor Red
    exit 1
}

# Check if remote already exists
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote -eq $githubUrl) {
    Write-Host "[OK] Remote 'origin' already set to: $githubUrl" -ForegroundColor Green
}
elseif ($null -ne $existingRemote) {
    Write-Host "[WARNING] Remote 'origin' already exists with different URL" -ForegroundColor Yellow
    Write-Host "   Existing: $existingRemote" -ForegroundColor Yellow
    $replace = Read-Host "Replace it? (yes/no)"
    if ($replace -eq "yes") {
        git remote remove origin
        git remote add origin $githubUrl
        Write-Host "[OK] Remote updated" -ForegroundColor Green
    }
    else {
        Write-Host "[SKIP] Skipping..." -ForegroundColor Yellow
    }
}
else {
    Write-Host "[SETUP] Adding remote origin..." -ForegroundColor Green
    git remote add origin $githubUrl
}

# Stage all files
Write-Host ""
Write-Host "[ACTION] Staging files..." -ForegroundColor Green
git add .

# Check for changes
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "[INFO] No changes to commit" -ForegroundColor Yellow
    exit 0
}

# Show what will be committed
Write-Host ""
Write-Host "[FILES] Files to commit:" -ForegroundColor Cyan
$status | ForEach-Object { Write-Host "   $_" }

# Commit
Write-Host ""
$commitMsg = Read-Host "Enter commit message (default: 'Initial Jobscraper release')"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Initial Jobscraper release"
}

Write-Host "[ACTION] Committing..." -ForegroundColor Green
git commit -m $commitMsg

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Commit failed" -ForegroundColor Red
    exit 1
}

# Set main branch
Write-Host ""
Write-Host "[SETUP] Setting main branch..." -ForegroundColor Green
git branch -M main

# Push to GitHub
Write-Host ""
Write-Host "[PUSH] Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Push failed" -ForegroundColor Red
    Write-Host "   Make sure your GitHub URL is correct and you have push permissions" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[SUCCESS] Your code is now on GitHub" -ForegroundColor Green
Write-Host ""
Write-Host "[URL] Repository: $githubUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "[NEXT] Next steps:" -ForegroundColor Cyan
Write-Host "   1. Deploy backend: heroku create jobscraper-backend" -ForegroundColor Gray
Write-Host "   2. Deploy frontend: cd frontend; vercel" -ForegroundColor Gray
Write-Host "   3. See DEPLOY_GITHUB.md for detailed instructions" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Deploy frontend: cd frontend; vercel" -ForegroundColor Gray
Write-Host "   3. See DEPLOY_GITHUB.md for detailed instructions" -ForegroundColor Gray
Write-Host ""
