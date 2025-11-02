from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from dotenv import load_dotenv
from backend import analysis
from backend import scraper

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "jobs.csv")

@app.route("/", methods=["GET"])
def index():
    """Root endpoint - return API info."""
    return jsonify({
        "message": "Job Web Scraper API",
        "endpoints": {
            "/health": "Health check",
            "/api/analysis": "Get job analysis",
            "/api/jobs": "Get all jobs",
            "/api/scrape": "Scrape new jobs (POST)",
            "/api/summary": "Generate summary (POST)"
        }
    }), 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """Return all jobs as JSON."""
    if not os.path.exists(DATA_PATH):
        return jsonify({"error": "No job data. Run /api/scrape first."}), 404
    df = pd.read_csv(DATA_PATH)
    return df.to_json(orient="records")

@app.route("/api/analysis", methods=["GET"])
def get_analysis():
    """Return analysis (top skills, salary stats)"""
    if not os.path.exists(DATA_PATH):
        return jsonify({"error": "No job data. Run /api/scrape first."}), 404
    df = pd.read_csv(DATA_PATH)
    result = analysis.analyze_jobs(df)
    return jsonify(result)

@app.route("/api/scrape", methods=["POST"])
def run_scrape():
    """Run a scrape from multiple sources.
    
    Request JSON:
    {
        "query": "python developer",
        "sources": ["remoteok", "himalayas"],  # optional, defaults to both APIs
        "pages": 1
    }
    """
    payload = request.get_json() or {}
    query = payload.get("query", "python developer")
    sources = payload.get("sources", ["remoteok", "himalayas", "remotive"])
    pages = int(payload.get("pages", 1))
    
    try:
        jobs = scraper.scrape_all(sources=sources, query=query, pages=pages)
        
        if not jobs:
            return jsonify({"status": "warning", "message": "No jobs found", "count": 0})
        
        # Save to CSV
        df = pd.DataFrame(jobs)
        df.to_csv(DATA_PATH, index=False)
        
        return jsonify({
            "status": "ok",
            "count": len(jobs),
            "message": f"Scraped {len(jobs)} jobs and saved to {DATA_PATH}"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/summary", methods=["POST"])
def career_summary():
    """Generate a career summary (simple or AI-powered via Gemini).
    
    Request JSON:
    {
        "use_ai": true,  # optional; if true, calls Gemini API
        "prompt": "custom prompt"  # optional; only used if use_ai=true
    }
    """
    if not os.path.exists(DATA_PATH):
        return jsonify({"error": "No job data. Run /api/scrape first."}), 404
    
    payload = request.get_json() or {}
    use_ai = payload.get("use_ai", False)
    custom_prompt = payload.get("prompt")
    
    df = pd.read_csv(DATA_PATH)
    
    if use_ai:
        summary = analysis.ai_summary_gemini(df, prompt=custom_prompt)
    else:
        summary = analysis.simple_text_summary(df)
    
    return jsonify({"summary": summary, "use_ai": use_ai})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") not in {"0", "false", "False"}
    app.run(host="0.0.0.0", port=port, debug=debug)
