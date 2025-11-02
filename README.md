# Job Data Scraper & AI Insights Dashboard

A full-stack job market analysis tool that scrapes job listings from multiple public sources, analyzes trends with pandas, and displays insights in a React dashboard. Includes optional AI-powered summaries via Google Gemini API.

## Features

- **Multi-source Scraping**: RemoteOK (API), Himalayas (API), Indeed (BeautifulSoup)
- **Data Analysis**: Top skills aggregation, salary statistics, trend detection
- **CSV Export**: Save scraped jobs to `jobs.csv`
- **React Dashboard**: Real-time visualization of market insights
- **AI Summaries** (optional): Google Gemini API integration for career insights
- **Rate-limiting**: Respect server limits and robots.txt
- **Error Handling**: Graceful fallbacks and logging

## Project Structure

```
Job Web Scraper/
├── backend/
│   ├── app.py              # Flask API server
│   ├── scraper.py          # Multi-source scraper (RemoteOK, Himalayas, Indeed)
│   ├── analysis.py         # Pandas analysis + Gemini integration
│   └── data/
│       ├── sample_jobs.csv # Sample data (for testing)
│       └── jobs.csv        # Output CSV from scraping
├── frontend/
│   ├── public/
│   │   └── index.html      # React entry point
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js          # Dashboard component
│   │   └── App.css
│   └── package.json
├── requirements.txt        # Python dependencies
├── README.md
└── .gitignore
```

## Quick Start

### 1. Backend Setup (Python)

**Create a Python virtual environment and install dependencies:**

```powershell
# From the Job Web Scraper folder
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Run the Flask API:**

```powershell
python -m backend.app
```

The backend runs on `http://localhost:5000` by default.

### 2. Test the Backend

**Using PowerShell (test the health endpoint):**

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health"
```

**Scrape jobs from RemoteOK and Himalayas:**

```powershell
$body = @{
    query = "python developer"
    sources = @("remoteok", "himalayas")
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/scrape" -Method POST -Body $body -ContentType "application/json"
```

**Get analysis (top skills, salary stats):**

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/analysis" -Method GET
```

**Get a simple summary:**

```powershell
$body = @{ use_ai = $false } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/api/summary" -Method POST -Body $body -ContentType "application/json"
```

### 3. Frontend Setup (Node.js / React)

**Install Node.js dependencies:**

```powershell
cd frontend
npm install
```

**Run the React dev server:**

```powershell
npm start
```

The frontend opens at `http://localhost:3000` by default.

## API Endpoints

### GET `/health`
Health check.

**Response:**
```json
{ "status": "healthy" }
```

---

### GET `/api/jobs`
Retrieve all scraped jobs.

**Response:**
```json
[
  {
    "title": "Data Scientist",
    "company": "Acme Analytics",
    "location": "Remote",
    "salary": "120000",
    "skills": "Python, SQL, Machine Learning",
    "description": "...",
    "date_posted": "2025-10-15",
    "source": "RemoteOK",
    "url": "https://..."
  },
  ...
]
```

---

### POST `/api/scrape`
Trigger a scrape from one or more sources.

**Request:**
```json
{
  "query": "python developer",
  "sources": ["remoteok", "himalayas"],
  "pages": 1
}
```

**Response:**
```json
{
  "status": "ok",
  "count": 42,
  "message": "Scraped 42 jobs and saved to ..."
}
```

---

### GET `/api/analysis`
Get aggregated analysis (top skills, salary stats).

**Response:**
```json
{
  "total_jobs": 42,
  "top_skills": [
    { "skill": "python", "count": 38 },
    { "skill": "sql", "count": 35 },
    { "skill": "machine learning", "count": 28 }
  ],
  "salary": {
    "mean": 125000,
    "median": 120000,
    "min": 80000,
    "max": 180000
  }
}
```

---

### POST `/api/summary`
Generate a career summary (simple or AI-powered).

**Request (simple):**
```json
{ "use_ai": false }
```

**Request (Gemini AI):**
```json
{
  "use_ai": true,
  "prompt": "Focus on AI/ML roles and skills needed in 2025"
}
```

**Response:**
```json
{
  "summary": "Based on market analysis... [AI-generated or simple text]",
  "use_ai": true
}
```

## Configuration

### Environment Variables

Create a `.env` file in the backend root (or set via PowerShell) to configure optional features:

```ini
# For Gemini AI summaries
GEMINI_API_KEY=your_gemini_api_key_here

# (Optional) Flask config
FLASK_ENV=development
FLASK_DEBUG=1
```

**PowerShell example:**
```powershell
$env:GEMINI_API_KEY = "sk-your-key-here"
python -m backend.app
```

### Scraper Sources

The scraper supports:

1. **RemoteOK** (`"remoteok"`)
   - Public JSON API (no auth)
   - ~50 jobs per query
   - Fast, no page parsing

2. **Himalayas** (`"himalayas"`)
   - Public JSON API (no auth)
   - Remote-focused jobs
   - Clean, structured data

3. **Indeed** (`"indeed"`)
   - BeautifulSoup scraper
   - Unlimited jobs (pageable)
   - Slower, respects robots.txt
   - Rate-limited to avoid overload

**Default:** Uses RemoteOK and Himalayas (fastest).

## AI Summaries with Google Gemini

### Setup

1. **Get a Gemini API key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a free API key (no billing required)

2. **Install optional dependency:**
   ```powershell
   pip install google-generativeai
   ```

3. **Set your API key:**
   ```powershell
   $env:GEMINI_API_KEY = "your_key_here"
   ```

4. **Use the API endpoint:**
   ```powershell
   $body = @{
       use_ai = $true
       prompt = "What are the top 5 most in-demand skills for AI/ML roles in 2025?"
   } | ConvertTo-Json
   
   Invoke-WebRequest -Uri "http://localhost:5000/api/summary" -Method POST -Body $body -ContentType "application/json" | ConvertFrom-Json | Select -ExpandProperty summary
   ```

## Example Workflows

### Workflow 1: Scrape and Analyze

```powershell
# 1. Scrape Python developer jobs
$scrapeBody = @{
    query = "python developer"
    sources = @("remoteok", "himalayas")
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/scrape" -Method POST -Body $scrapeBody -ContentType "application/json"

# 2. Get analysis
$analysis = Invoke-WebRequest -Uri "http://localhost:5000/api/analysis" | ConvertFrom-Json
$analysis.top_skills | Select -First 5

# 3. Get AI summary (if Gemini key is set)
$summaryBody = @{ use_ai = $true } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/api/summary" -Method POST -Body $summaryBody -ContentType "application/json" | ConvertFrom-Json | Select -ExpandProperty summary
```

### Workflow 2: Export to CSV and Analyze Locally

```powershell
# Scrape jobs
$scrapeBody = @{
    query = "data scientist"
    sources = @("remoteok", "himalayas", "indeed")
    pages = 2
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/scrape" -Method POST -Body $scrapeBody -ContentType "application/json"

# The jobs are now in backend/data/jobs.csv
# Open in Excel or pandas
```

## Ethical Scraping

- **RemoteOK & Himalayas**: Use public APIs (recommended).
- **Indeed**: Respects robots.txt and rate-limits (safe to scrape public search pages).
- **LinkedIn**: Do NOT scrape; violates ToS. Use official API instead.
- **Rate-limiting**: Built in; requests are throttled.

## Troubleshooting

### No jobs returned
- Check internet connection
- Verify API endpoints are accessible (e.g., `https://remoteok.com/api` returns JSON)
- Try a different query or add "indeed" source (slower but usually finds results)

### "No job data" error
- Run `/api/scrape` first to populate the database
- Check that `backend/data/jobs.csv` exists

### Gemini API errors
- Verify `GEMINI_API_KEY` is set
- Check that `google-generativeai` is installed: `pip install google-generativeai`
- Ensure the API key is valid

### Frontend won't connect to backend
- Ensure Flask app is running on port 5000
- Check CORS is enabled in `app.py` (it is)
- Open browser console for error details

## Performance Notes

- **First scrape**: 10–30 seconds (depends on sources and query)
- **Subsequent API calls**: <1 second (reads from cached CSV)
- **AI summary generation**: 3–10 seconds (calls Gemini API)

## Future Enhancements

- [ ] Database (PostgreSQL) instead of CSV
- [ ] Scheduled scraping (daily/hourly)
- [ ] More job sites (LinkedIn API, GitHub Jobs, etc.)
- [ ] Skill matching and recommendations
- [ ] Dashboard charts (React-Vis, Chart.js)
- [ ] Authentication & user saved queries

## License

MIT
