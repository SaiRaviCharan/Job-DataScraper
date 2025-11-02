# Quick Start Guide - Job Web Scraper

## 🚀 Get Started in 2 Minutes

### Prerequisites
- Python 3.8+
- Node.js 14+

### Step 1: Start the Backend

Open PowerShell in the `S:\Job Web Scraper` folder and run:

```powershell
.\run_backend.ps1
```

Or manually:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m backend.app
```

✓ The API is now running on `http://localhost:5000`

### Step 2: Start the Frontend

Open a **new PowerShell** window in the same folder and run:

```powershell
.\run_frontend.ps1
```

Or manually:

```powershell
cd frontend
npm install
npm start
```

✓ The dashboard opens on `http://localhost:3000`

### Step 3: Scrape Jobs

In the dashboard, enter a search query (e.g., "python developer") and click **⚡ Scrape Jobs**.

The app will fetch jobs from RemoteOK and Himalayas, then display:
- Total jobs analyzed
- Average/min/max salaries
- Top in-demand skills
- Career insights

### Step 4 (Optional): Enable AI Summaries

1. Get a free Gemini API key: https://makersuite.google.com/app/apikey
2. Set environment variable in PowerShell:
   ```powershell
   $env:GEMINI_API_KEY = "your_key_here"
   ```
3. Restart the backend
4. Click **✨ Generate AI Summary** in the dashboard

---

## 📊 Test the API Directly

Run the test script:

```powershell
.\test_api.ps1
```

This will:
- Scrape 50 jobs
- Fetch analysis (top skills + salaries)
- Generate summaries

---

## 📁 What's Included

- **backend/app.py** → Flask REST API
- **backend/scraper.py** → RemoteOK, Himalayas, Indeed scrapers
- **backend/analysis.py** → Pandas analytics + Gemini AI
- **frontend/src/App.js** → React dashboard
- **requirements.txt** → Python dependencies
- **run_backend.ps1** → Helper script to start the backend
- **run_frontend.ps1** → Helper script to start the frontend
- **test_api.ps1** → Example API calls

---

## 🔗 API Endpoints

```
GET /health                  → Health check
GET /api/jobs               → List all jobs
GET /api/analysis           → Top skills + salary stats
POST /api/scrape            → Scrape new jobs
POST /api/summary           → Text or AI summary
```

See `README.md` for detailed docs.

---

## ⚡ Common Issues

**"No job data"**
→ Run `/api/scrape` first or click the scraper button in the dashboard

**"Can't connect to backend"**
→ Make sure `python -m backend.app` is running on port 5000

**AI summary not working**
→ Set `GEMINI_API_KEY` environment variable with a valid API key

**Frontend won't start**
→ Install Node.js and run `npm install` in the frontend folder

---

## 📚 Next Steps

- Add more job sources (LinkedIn API, GitHub Jobs, etc.)
- Store jobs in PostgreSQL instead of CSV
- Add job matching based on your skills
- Create scheduled scraping (daily/hourly)
- Deploy to Heroku or Vercel

Enjoy! 🎉
