# Jobscraper - Deploy to GitHub, Heroku & Vercel

## Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and log in
2. Click **+** (top right) → **New repository**
3. Name it `jobscraper` (or your choice)
4. Set to **Public** (or Private if you prefer)
5. **Do NOT** initialize with README (you already have one)
6. Click **Create repository**
7. Copy the HTTPS URL shown (e.g., `https://github.com/yourusername/jobscraper.git`)

## Step 2: Push Local Code to GitHub

Open PowerShell in `S:\Job Web Scraper`:

```powershell
# Initialize git repo (first time only)
git init

# Add all files
git add .

# First commit
git commit -m "Initial Jobscraper release"

# Add remote (paste YOUR URL from step 1.7)
git remote add origin https://github.com/yourusername/jobscraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verify**: Refresh GitHub page—your code should appear.

---

## Step 3: Deploy Backend to Heroku

### 3a. Install & Login

```powershell
# Install Heroku CLI (if not already)
# Download from https://devcenter.heroku.com/articles/heroku-cli

heroku login
# Browser opens → log in to Heroku
```

### 3b. Create App & Deploy

```powershell
# From S:\Job Web Scraper directory
heroku create jobscraper-backend

# Push main branch to Heroku
git push heroku main

# Set environment variables
heroku config:set GEMINI_API_KEY=your_actual_key_here
heroku config:set FLASK_DEBUG=0

# Scale dyno (free tier = 1)
heroku ps:scale web=1

# Open app in browser
heroku open

# Watch logs for errors
heroku logs --tail
```

**Expected Output**:
```
✓ https://jobscraper-backend.herokuapp.com/
```

**Test it**: Visit `https://jobscraper-backend.herokuapp.com/health` in browser.

---

## Step 4: Deploy Frontend to Vercel

### 4a. Install & Login

```powershell
# Install Vercel CLI
npm install -g vercel

# Log in
vercel login
# Browser opens → connect GitHub account
```

### 4b. Deploy

```powershell
# Go to frontend folder
cd frontend

# First deployment (creates project)
vercel

# Answer prompts:
# - Link to existing project? No
# - Project name? jobscraper-frontend
# - Framework? React
# - Root directory? ./
# - Build settings? Default (npm run build)
```

### 4c. Set Backend URL

```powershell
# Add environment variable
vercel env add REACT_APP_API_BASE

# When prompted, paste: https://jobscraper-backend.herokuapp.com
# (or your actual Heroku URL from Step 3)

# Deploy to production
vercel --prod
```

**Expected Output**:
```
✓ https://jobscraper-frontend.vercel.app/ (production)
```

---

## Step 5: Verify Everything Works

1. **Open frontend**: `https://jobscraper-frontend.vercel.app/`
2. **Search for jobs**: Type "python" → click **⚡ Scrape Jobs**
3. **Watch Heroku logs**: `heroku logs --tail` (in another PowerShell)
4. **Confirm API calls**: Should see requests in Heroku logs
5. **Check results**: Dashboard should display jobs, skills, analysis

---

## Step 6: Set Up Auto-Deploy (Optional)

### GitHub → Heroku Auto-Deploy

```powershell
# In S:\Job Web Scraper, connect repo to Heroku
heroku git:remote -a jobscraper-backend

# Now every `git push heroku main` auto-deploys
git push heroku main
```

### GitHub → Vercel Auto-Deploy

In Vercel Dashboard:
1. Go to **Settings** → **Git**
2. Link GitHub repo
3. Set **Production Branch** to `main`
4. Enable **Automatic Deployments**
5. Now every GitHub push auto-builds Vercel

---

## Step 7: Lock Down Secrets

### Add `.gitignore` (if missing)

Create `S:\Job Web Scraper\.gitignore`:
```
.env
.env.local
node_modules/
.venv/
__pycache__/
*.pyc
.DS_Store
```

Then:
```powershell
git add .gitignore
git commit -m "Add gitignore"
git push origin main
```

**Never commit `.env` to GitHub** (it contains your API key).

---

## Step 8: Document Live URLs

Create a `LIVE_DEPLOYMENT.md` in repo root:

```markdown
# Jobscraper - Live Deployment

## URLs

- **Frontend**: https://jobscraper-frontend.vercel.app/
- **Backend API**: https://jobscraper-backend.herokuapp.com/
- **Repository**: https://github.com/yourusername/jobscraper

## Configuration

- Backend: Heroku (auto-deploys from `git push heroku main`)
- Frontend: Vercel (auto-deploys from GitHub main branch)

## Environment Variables

### Heroku (Backend)
```
GEMINI_API_KEY=<your-key>
FLASK_DEBUG=0
```

### Vercel (Frontend)
```
REACT_APP_API_BASE=https://jobscraper-backend.herokuapp.com
```

## Monitoring

- Backend logs: `heroku logs --tail`
- Frontend logs: Vercel Dashboard → Deployments
- Errors: Check `.env` setup; ensure GEMINI_API_KEY is set
```

Commit & push:
```powershell
git add LIVE_DEPLOYMENT.md
git commit -m "Add live deployment info"
git push origin main
```

---

## Troubleshooting

### Frontend shows "API Error"
- Check Vercel env var `REACT_APP_API_BASE`
- Rebuild: `vercel --prod`

### Backend won't start on Heroku
- Check logs: `heroku logs --tail`
- Verify env vars: `heroku config`
- Redeploy: `git push heroku main`

### "buildpack" error
- Heroku auto-detects Python from `runtime.txt`
- Confirm file exists: `cat runtime.txt` → should say `python-3.11.9`

### GitHub push fails
- Check remote: `git remote -v`
- Verify credentials: `git config user.email` / `user.name`
- Fix: `git config user.email "your@email.com"` + retry

---

## Next Steps

1. ✅ Share GitHub link with friends/portfolio
2. ✅ Add custom domain (optional Heroku/Vercel feature)
3. ✅ Set up email alerts on errors (Heroku Alerts)
4. ✅ Monitor API usage (free tier limits apply)
5. ✅ Deploy Phase 2 features (DB, auth, etc.)

**Done! Your Jobscraper is live.** 🚀
