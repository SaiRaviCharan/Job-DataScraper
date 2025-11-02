# Jobscraper

**Status:** ✅ **Production-ready** (ready to run and deploy)

## What You've Got

A full-stack job market intelligence platform with:

```

Expected output:
```

✓ Node.js found: vxx.x.x
✓ Starting React dev server on http://localhost:3000...
```

### 3️⃣ Use the Dashboard

- Open http://localhost:3000 in your browser
- Enter a search query (e.g., "python developer")
- Click **⚡ Scrape Jobs**
- View analysis: skills, salaries, trends
- Generate summaries (simple or AI-powered)

---


Health check endpoint.


### POST `/api/scrape`
Scrape jobs from one or more sources.

**Request:**

  "pages": 1
}

{
  "status": "ok",

```

---

### GET `/api/analysis`
Get aggregated analysis (top skills, salary stats).

## 🐛 Troubleshooting

### Backend won't start

```powershell
# Check Python installation
python --version

# Check pip
pip --version

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start

```powershell
# Check Node.js installation
node --version

# Clear npm cache
npm cache clean --force

# Reinstall packages
cd frontend
rm -r node_modules
npm install
```

### No jobs found after scraping

- API may be down temporarily (try again)
- Query too specific (try "python" instead of "python senior developer")
- Rate-limit hit (wait 10 seconds and try again)

### Gemini API errors

- Check API key is valid: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- Install library: `pip install google-generativeai`
- Check internet connection
- API quota exceeded (free tier limits apply)

---

## 📈 Future Enhancements

### Phase 2

- [ ] PostgreSQL database (instead of CSV)
- [ ] User authentication (sign up, save queries)
- [ ] Scheduled scraping (daily/hourly)
- [ ] More job sources (GitHub Jobs, DevOps, Stack Overflow)

### Phase 3

- [ ] Job-to-profile matching (upload your resume, get recommendations)
- [ ] Salary comparison by location/role
- [ ] Trend prediction (ML model to forecast skill demand)
- [ ] Email alerts (daily digest of new jobs)

### Phase 4

- [ ] Mobile app (React Native)
- [ ] Browser extension (job posting notifications)
- [ ] Slack integration
- [ ] Webhook support

---

## 📞 Support & Feedback

### Common Questions

**Q: Can I scrape LinkedIn?**
A: No, LinkedIn's ToS prohibits scraping. Use their official API or alternatives like RemoteOK, Indeed, etc.

**Q: How many jobs can I scrape?**
A: Depends on the source. RemoteOK/Himalayas: ~50–100 per query. Indeed: Unlimited (pageable).

**Q: Is my data private?**
A: All data is stored locally in `backend/data/jobs.csv`. No external upload unless you explicitly integrate a backend database.

**Q: Can I use this commercially?**
A: Yes, but respect each job site's ToS and robots.txt. APIs like RemoteOK are free for small-scale use.

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## ✨ What's Next?

1. Run the quick start: `.
un_backend.ps1` (new terminal) + `.
un_frontend.ps1`
2. Test the API: `.	est_api.ps1`
3. Explore the dashboard: [http://localhost:3000](http://localhost:3000)
4. Configure Gemini API for AI summaries
5. Deploy to cloud (Heroku, Vercel, etc.)

Enjoy building! 🚀

Or set in PowerShell:

```powershell
$env:GEMINI_API_KEY = "your_key_here"
python -m backend.app
```

### Scraper Configuration

Available sources:
- **remoteok**: Fast, API-based, no auth (recommended)
- **himalayas**: Fast, API-based, remote jobs (recommended)
- **indeed**: Slower, page-based, unlimited results

Default: Uses RemoteOK and Himalayas (fastest).

---

## 🔧 Tech Stack Details

### Backend
- **Framework**: Flask (lightweight, perfect for small-to-medium projects)
- **Data**: Pandas (aggregation, analysis, CSV export)
- **Scraping**: 
  - requests (HTTP client)
  - BeautifulSoup4 (HTML parsing for Indeed)
- **API Clients**:
  - RemoteOK: Direct JSON endpoint
  - Himalayas: Direct JSON endpoint
  - Google Gemini: google-generativeai library
- **CORS**: flask-cors (enables frontend requests)

### Frontend
- **Framework**: React 18 (modern, hooks-based)
- **Styling**: CSS3 (gradients, grid, flexbox, responsive)
- **HTTP**: Fetch API (native, no extra library needed)
- **Build**: react-scripts (Create React App)

### Data Flow
```
Frontend (React)
    ↓
    ↓ fetch('http://localhost:5000/api/...')
    ↓
Backend (Flask)
    ├─ Scraper (requests + BeautifulSoup)
    ├─ RemoteOK API
    ├─ Himalayas API
    ├─ Indeed HTML parsing
    └─ CSV / Analysis (Pandas)
         ↓
         ↓ Gemini API (optional AI summary)
         ↓
         JSON response
    ↓ (returned to Frontend)
    ↓
Frontend renders: skills, salaries, insights
```

---

## 📊 Performance Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| Scrape from APIs | 10–30s | Depends on query and network |
| Read CSV & analyze | <1s | Fast pandas operations |
| API response | <100ms | JSON serialization |
| AI summary (Gemini) | 3–10s | Depends on API quota |
| Frontend load | <2s | React dev server |

---

## 🛡️ Ethical & Legal Notes

✅ **Safe Scraping:**
- RemoteOK & Himalayas: Use public APIs (no scraping needed)
- Indeed: Respects robots.txt, rate-limited
- Rate-limiting: 0.5–1.0s between requests

❌ **DO NOT:**
- Scrape LinkedIn (violates ToS)
- Remove attribution
- Ignore robots.txt
- Spam APIs with excessive requests

---

## 🔐 Security

- **CORS**: Enabled (frontend can access backend)
- **Rate-limiting**: Built-in delays between requests
- **Error handling**: No sensitive data leaked in error messages
- **Environment vars**: Use `.env` for API keys (not hardcoded)

---

## 🚀 Deployment (Quick Guide)

### Deploy Backend to Heroku

> Prerequisites: [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), a Heroku account, and Git installed.

```bash
# 1. Login and create the app
heroku login
heroku create your-job-scraper

# 2. Push code (Procfile & runtime.txt already included)
git push heroku main

# 3. Configure environment
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set FLASK_DEBUG=0

# 4. Scale dyno
heroku ps:scale web=1

# 5. Verify
heroku open
heroku logs --tail
```

### Deploy Frontend to Vercel

```bash
# Navigate to frontend folder
cd frontend

# Deploy
npm install -g vercel
vercel

# Set environment variable for production build
vercel env add REACT_APP_API_BASE
# (paste https://your-job-scraper.herokuapp.com)

# For local production build previews
npm run build
```

> ⚙️ **Remember:** The React app reads `REACT_APP_API_BASE`. Set it to your deployed backend URL (e.g., `https://your-job-scraper.herokuapp.com`).
