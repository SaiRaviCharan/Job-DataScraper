# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              React Dashboard (Frontend)                      │  │
│  │  http://localhost:3000                                       │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │  Header: Job Insights Dashboard                     │   │  │
│  │  │  - Search bar (query input)                         │   │  │
│  │  │  - "⚡ Scrape Jobs" button                          │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │  Market Overview                                    │   │  │
│  │  │  - Total jobs analyzed (stat card)                 │   │  │
│  │  │  - Average salary (stat card)                      │   │  │
│  │  │  - Min/Max salary (stat cards)                     │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │  Top In-Demand Skills                              │   │  │
│  │  │  #1 Python ████████████████ (38)                   │   │  │
│  │  │  #2 SQL ██████████████ (35)                        │   │  │
│  │  │  #3 ML ███████████ (28)                            │   │  │
│  │  │  ...                                               │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │  Career Insights                                   │   │  │
│  │  │  - Summary text box                                │   │  │
│  │  │  - "📝 Simple Summary" button                      │   │  │
│  │  │  - "✨ AI Summary" button                          │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                                                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↕ (HTTP)
                    fetch('http://localhost:5000/api/...')
                              ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER (Python)                          │
│                  http://localhost:5000                              │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Flask REST API (app.py)                                    │  │
│  │                                                             │  │
│  │  GET /health              → {"status": "healthy"}          │  │
│  │  POST /api/scrape         → Trigger scrape               │  │
│  │  GET /api/jobs            → List all jobs                │  │
│  │  GET /api/analysis        → Skills + salaries            │  │
│  │  POST /api/summary        → Text or AI summary           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│           ↕ (calls modules)          ↕ (calls modules)            │
│    ┌──────────────────────────┐  ┌──────────────────────────┐     │
│    │  Scraper (scraper.py)    │  │ Analysis (analysis.py)   │     │
│    │                          │  │                          │     │
│    │ scrape_remoteok()        │  │ analyze_jobs()           │     │
│    │ scrape_himalayas()       │  │ simple_text_summary()    │     │
│    │ scrape_indeed()          │  │ ai_summary_gemini()      │     │
│    │ scrape_all()             │  │ parse_skills()           │     │
│    │ scrape_dummy()           │  │                          │     │
│    └──────────────────────────┘  └──────────────────────────┘     │
│           ↕ (network calls)             ↕ (data I/O)              │
│    ┌──────────────────────────┐  ┌──────────────────────────┐     │
│    │  External APIs           │  │  CSV File                │     │
│    │                          │  │                          │     │
│    │ RemoteOK API (JSON)      │  │ jobs.csv                 │     │
│    │ ├─ GET remoteok.com/api  │  │ ├─ title                 │     │
│    │ └─ Parse + normalize     │  │ ├─ company               │     │
│    │                          │  │ ├─ salary                │     │
│    │ Himalayas API (JSON)     │  │ ├─ skills                │     │
│    │ ├─ GET himalayas.app/api │  │ ├─ location              │     │
│    │ └─ Parse + normalize     │  │ └─ ...                   │     │
│    │                          │  │                          │     │
│    │ Indeed (HTML)            │  │ ↓ (Pandas read/write)    │     │
│    │ ├─ GET indeed.com/jobs   │  │ ↓ (Analysis)             │     │
│    │ ├─ BeautifulSoup parse   │  │                          │     │
│    │ └─ Extract fields        │  │  ↓ (optional)            │     │
│    │                          │  │ Google Gemini API        │     │
│    │ (Rate-limited 0.5–1s)    │  │ ├─ POST api.generativeai │     │
│    │                          │  │ └─ Generate summary      │     │
│    └──────────────────────────┘  └──────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Scraping Flow

```
User clicks "Scrape Jobs" (query: "python developer")
    ↓
Frontend: POST /api/scrape {query, sources, pages}
    ↓
Backend app.py: run_scrape()
    ↓
scraper.scrape_all(["remoteok", "himalayas"])
    ├─ scraper.scrape_remoteok("python developer")
    │  ├─ requests.get("https://remoteok.com/api")
    │  └─ Parse JSON + normalize → [jobs...]
    │
    └─ scraper.scrape_himalayas("python developer")
       ├─ requests.get("https://himalayas.app/api/v1/jobs")
       └─ Parse JSON + normalize → [jobs...]
    ↓
Combine results → [job1, job2, job3, ...]
    ↓
Save to CSV: backend/data/jobs.csv
    ↓
Return: {status: "ok", count: N, message: "Scraped N jobs"}
    ↓
Frontend: Alert success + refresh analysis
```

### Analysis Flow

```
User views dashboard (or clicks "Generate Summary")
    ↓
Frontend: GET /api/analysis
    ↓
Backend app.py: get_analysis()
    ↓
Load CSV: pd.read_csv("jobs.csv")
    ↓
analysis.analyze_jobs(df)
    ├─ Parse skills (normalize, split by comma)
    ├─ Counter.most_common(20) → top skills
    ├─ Salary extraction (remove $, convert to float)
    └─ Calculate: mean, median, min, max
    ↓
Return JSON:
{
  "total_jobs": 42,
  "top_skills": [
    {"skill": "python", "count": 38},
    {"skill": "sql", "count": 35}
  ],
  "salary": {
    "mean": 125000,
    "median": 120000,
    "min": 80000,
    "max": 180000
  }
}
    ↓
Frontend: Render cards + skills list + charts
```

### AI Summary Flow (Optional)

```
User clicks "Generate AI Summary"
    ↓
Frontend: POST /api/summary {use_ai: true}
    ↓
Backend app.py: career_summary()
    ├─ Load CSV
    ├─ Call analysis.ai_summary_gemini(df)
    │  ├─ Extract top skills, salary stats
    │  ├─ Build prompt
    │  ├─ genai.configure(api_key)
    │  ├─ model.generate_content(prompt)
    │  └─ Return AI response
    │
    └─ Return JSON: {summary: "...", use_ai: true}
    ↓
Frontend: Display in summary text box
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│                                                              │
│  App Component                                              │
│  ├─ state: analysis, summary, query, useAI, loading       │
│  │                                                         │
│  ├─ useEffect → fetch /api/analysis (on mount)           │
│  │                                                         │
│  ├─ handleScrape()                                        │
│  │  └─ POST /api/scrape → refresh analysis              │
│  │                                                         │
│  ├─ fetchAnalysis()                                       │
│  │  └─ GET /api/analysis → setAnalysis(data)            │
│  │                                                         │
│  ├─ fetchSummary(useGemini)                             │
│  │  └─ POST /api/summary → setSummary(data.summary)     │
│  │                                                         │
│  └─ render: Header + Scraper + Stats + Skills + Summary  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask)                           │
│                                                              │
│  app.py                                                      │
│  ├─ app = Flask(__name__)                                  │
│  ├─ CORS(app)                                              │
│  │                                                         │
│  ├─ @app.route('/api/scrape', methods=['POST'])          │
│  │  ├─ payload = request.get_json()                      │
│  │  ├─ jobs = scraper.scrape_all(...)                   │
│  │  ├─ df.to_csv(DATA_PATH)                             │
│  │  └─ return {status, count, message}                 │
│  │                                                         │
│  ├─ @app.route('/api/analysis', methods=['GET'])        │
│  │  ├─ df = pd.read_csv(DATA_PATH)                      │
│  │  ├─ result = analysis.analyze_jobs(df)               │
│  │  └─ return jsonify(result)                           │
│  │                                                         │
│  ├─ @app.route('/api/summary', methods=['POST'])        │
│  │  ├─ use_ai = payload.get('use_ai')                   │
│  │  ├─ if use_ai:                                        │
│  │  │  └─ summary = analysis.ai_summary_gemini(df)     │
│  │  ├─ else:                                             │
│  │  │  └─ summary = analysis.simple_text_summary(df)   │
│  │  └─ return {summary, use_ai}                        │
│  │                                                         │
│  └─ if __name__ == '__main__':                          │
│     └─ app.run(host='0.0.0.0', port=5000, debug=True) │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
Development (Local)
├─ Frontend: http://localhost:3000 (React dev server)
├─ Backend: http://localhost:5000 (Flask debug server)
└─ Data: backend/data/jobs.csv (local filesystem)

Production (Cloud)
├─ Frontend: https://your-app.vercel.app (Vercel)
├─ Backend: https://your-api.herokuapp.com (Heroku)
└─ Data: PostgreSQL database (Cloud)
    └─ (Optional: migrate from CSV)
```

---

**Architecture is modular, scalable, and production-ready!**
