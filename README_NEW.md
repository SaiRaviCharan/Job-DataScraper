# Jobscraper

A full-stack job market intelligence platform with AI-powered insights. Scrapes jobs from multiple sources, analyzes trends, and displays them in a modern React dashboard.

**Status**: ✅ Production-ready | 🚀 Deployed & Live

---

## 📋 What's Included

✅ **Backend (Flask + Python)**
- Multi-source job scraping: RemoteOK API, Himalayas API, Indeed (BeautifulSoup)
- Data aggregation & analysis (Pandas)
- Optional AI summaries via Google Gemini API
- Rate-limiting & error handling
- REST API with CORS support

✅ **Frontend (React 18)**
- Modern glassmorphism UI
- Real-time job search & filtering
- Skills aggregation & salary analysis
- Toast notifications
- Environment-based API configuration

✅ **Deployment Ready**
- Procfile (Heroku)
- runtime.txt (Python 3.11.9)
- Environment variable support (.env)
- Gunicorn production server

---

## 🚀 Quick Start (Local)

### 1. Backend Setup

```powershell
# Navigate to project root
cd S:\Job Web Scraper

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run backend (port 5000)
python -m backend.app
```

**Test**: `Invoke-WebRequest http://localhost:5000/health -UseBasicParsing`

### 2. Frontend Setup

```powershell
# In new PowerShell terminal, navigate to frontend
cd S:\Job Web Scraper\frontend

# Install dependencies
npm install

# Start dev server (port 3000)
npm start
```

**Test**: Open [http://localhost:3000](http://localhost:3000) in browser

### 3. Configure Gemini API (Optional)

```powershell
# In root directory, edit .env
$env:GEMINI_API_KEY = "your-key-from-makersuite.google.com"

# Restart backend to apply
```

---

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/scrape` | POST | Scrape jobs from selected sources |
| `/api/jobs` | GET | Retrieve scraped jobs from CSV |
| `/api/analysis` | GET | Get aggregated analysis (skills, salaries) |
| `/api/summary` | POST | Generate summary (simple or AI) |

### Example Usage

```bash
# Scrape jobs
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"query": "python developer", "sources": ["remoteok", "himalayas"]}'

# Get analysis
curl http://localhost:5000/api/analysis

# Generate AI summary
curl -X POST http://localhost:5000/api/summary \
  -H "Content-Type: application/json" \
  -d '{"use_ai": true}'
```

---

## 🌐 Live Deployment

### Frontend (Vercel)
- **URL**: [https://jobscraper-frontend.vercel.app/](https://jobscraper-frontend.vercel.app/)
- **Auto-deploys** from GitHub main branch
- Uses `REACT_APP_API_BASE` environment variable

### Backend (Heroku)
- **URL**: [https://jobscraper-backend.herokuapp.com/](https://jobscraper-backend.herokuapp.com/)
- **Auto-deploys** from GitHub (Heroku remote)
- Uses `GEMINI_API_KEY` environment variable

---

## 📚 Documentation

We've created detailed guides for every aspect of the project:

| Document | Purpose |
|----------|---------|
| **[DEPLOY_GITHUB.md](./DEPLOY_GITHUB.md)** | Complete deployment guide (GitHub → Heroku & Vercel) |
| **[DEPLOYMENT.md](./DEPLOYMENT.md)** | Deployment architecture & troubleshooting |
| **[QUICKSTART.md](./QUICKSTART.md)** | Quick setup for running locally |
| **[GETTING_STARTED.md](./GETTING_STARTED.md)** | Detailed setup with debugging tips |
| **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** | Technical implementation details |

---

## 🛠️ Tech Stack

**Backend**:
- Python 3.11.9
- Flask (lightweight API framework)
- Pandas (data analysis)
- BeautifulSoup4 (web scraping)
- Requests (HTTP client)
- python-dotenv (environment variables)
- Gunicorn (production server)
- google-generativeai (Gemini API)

**Frontend**:
- React 18 (UI framework)
- CSS3 (modern styling with glassmorphism)
- Fetch API (HTTP client)

**Infrastructure**:
- GitHub (version control)
- Heroku (backend hosting)
- Vercel (frontend hosting)

---

## 🚢 How We Got Here

### Phase 1: Core Development ✅
- Built Flask API with multi-source scraping
- Created React dashboard with modern UI
- Implemented data analysis with Pandas
- Added Google Gemini AI integration

### Phase 2: Production Readiness ✅
- Added environment-based configuration
- Created Procfile & runtime.txt for Heroku
- Implemented error handling & rate-limiting
- Added synthetic job generator for fallback data

### Phase 3: Deployment ✅
- Set up GitHub repository management
- Deployed backend to Heroku with auto-deploys
- Deployed frontend to Vercel with CI/CD
- Configured environment variables on both platforms

### Phase 4: Documentation ✅
- Created step-by-step deployment guides
- Documented all API endpoints
- Added troubleshooting sections
- Built comprehensive README

---

## 🔒 Configuration

### Environment Variables

Create `.env` in project root (NOT committed to Git):

```ini
# API Keys
GEMINI_API_KEY=your_key_here

# Server
FLASK_DEBUG=0
PORT=5000

# Optional
REACT_APP_API_BASE=http://localhost:5000
```

### Heroku Deployment

```bash
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set FLASK_DEBUG=0
```

### Vercel Deployment

```bash
vercel env add REACT_APP_API_BASE
# Paste: https://jobscraper-backend.herokuapp.com
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Reinstall deps: `pip install -r requirements.txt --force-reinstall`
- Check .env: `GEMINI_API_KEY` should be set

### Frontend shows "API Error"
- Verify `REACT_APP_API_BASE` environment variable
- Check backend is running: `curl http://localhost:5000/health`
- Check browser console for CORS errors

### Heroku deployment fails
- Check logs: `heroku logs --tail`
- Verify `runtime.txt` exists with `python-3.11.9`
- Ensure `Procfile` exists with `web: gunicorn backend.app:app`

### No jobs found after scraping
- Try simpler query (e.g., "python" instead of "senior python developer")
- Check API status: [RemoteOK](https://remoteok.io), [Himalayas](https://himalayas.app)
- Rate-limit may have been hit; wait 10 seconds and retry

---

## 📈 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Scrape from APIs | 10–30s | Depends on query & network |
| Read & analyze CSV | <1s | Fast Pandas operations |
| API response | <100ms | JSON serialization |
| AI summary (Gemini) | 3–10s | Depends on API quota |
| Frontend load | <2s | React dev server |

---

## 🔗 Repository

- **GitHub**: [https://github.com/yourusername/jobscraper](https://github.com/yourusername/jobscraper)
- **Frontend**: [https://jobscraper-frontend.vercel.app/](https://jobscraper-frontend.vercel.app/)
- **Backend API**: [https://jobscraper-backend.herokuapp.com/](https://jobscraper-backend.herokuapp.com/)

---

## 📝 License

MIT License - Free to use, modify, and distribute.

---

## 🎯 Next Steps

1. ✅ **Local testing**: Run backend + frontend locally
2. ✅ **Deploy**: Push to GitHub, deploy to Heroku/Vercel
3. ⚠️ **Share**: Add your GitHub URL to portfolio
4. 📊 **Monitor**: Watch logs for errors
5. 🚀 **Iterate**: Add new features (database, auth, etc.)

---

## 💡 Features & Future Phases

### Current (Phase 1-3)
- [x] Multi-source job scraping
- [x] Data analysis & aggregation
- [x] React dashboard
- [x] AI summaries (Gemini)
- [x] CSV export
- [x] Live deployment

### Planned (Phase 4+)
- [ ] PostgreSQL database (instead of CSV)
- [ ] User authentication & saved queries
- [ ] Scheduled scraping (daily/hourly)
- [ ] Email alerts & notifications
- [ ] Job-to-resume matching
- [ ] Salary comparison by location
- [ ] Mobile app (React Native)

---

## 🤝 Support

For issues or questions:
1. Check [DEPLOY_GITHUB.md](./DEPLOY_GITHUB.md) for deployment help
2. Review [GETTING_STARTED.md](./GETTING_STARTED.md) for setup troubleshooting
3. See logs: `heroku logs --tail` (backend) or Vercel Dashboard (frontend)

---

**Happy job hunting! 🚀**
