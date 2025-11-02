"""Pandas-based analysis utilities for job listings.

Provides:
- parse_skills: normalize skills strings into lists
- analyze_jobs: returns top skills and salary stats
- simple_text_summary: small human-readable summary
"""

import pandas as pd
from collections import Counter
import numpy as np

# Preferred Gemini model ids in fallback order (newest first).
_GEMINI_MODEL_CANDIDATES = [
    # Gemini 2.0 models are available on the free tier.
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite-001",
    "models/gemini-2.0-flash-exp",
    "models/gemini-2.0-flash-lite-preview",
    "models/gemini-2.0-flash-lite-preview-02-05",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]


def _extract_gemini_text(response):
    """Return best-effort text output from a Gemini response object."""
    text = getattr(response, "text", None)
    if text:
        return text

    parts = []
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            part_text = getattr(part, "text", None)
            if part_text:
                parts.append(part_text)

    return "\n".join(parts) if parts else ""


def parse_skills(skills_field):
    """Turn a skills string (comma-separated) into a normalized list."""
    if pd.isna(skills_field):
        return []
    if isinstance(skills_field, (list, tuple)):
        return [s.strip().lower() for s in skills_field]
    parts = [p.strip().lower() for p in str(skills_field).split(",") if p.strip()]
    return parts


def analyze_jobs(df: pd.DataFrame):
    """Return a JSON-serializable dict with top skills and salary stats."""
    df = df.copy()

    # Normalize salary to numeric where possible
    def to_numeric_salary(s):
        try:
            return float(str(s).replace("$", "").replace(",", ""))
        except Exception:
            return np.nan

    df["salary_num"] = df.get("salary").apply(to_numeric_salary)

    # Skills
    all_skills = Counter()
    for s in df.get("skills", []):
        items = parse_skills(s)
        all_skills.update(items)

    top_skills = [
        {"skill": skill, "count": count}
        for skill, count in all_skills.most_common(20)
    ]

    # Salary statistics (ignore NaN)
    salary_series = df["salary_num"].dropna().astype(float)
    if len(salary_series) > 0:
        salary_stats = {
            "mean": round(float(salary_series.mean()), 2),
            "median": round(float(salary_series.median()), 2),
            "min": round(float(salary_series.min()), 2),
            "max": round(float(salary_series.max()), 2),
        }
    else:
        salary_stats = {"mean": None, "median": None, "min": None, "max": None}

    return {
        "total_jobs": int(len(df)),
        "top_skills": top_skills,
        "salary": salary_stats,
    }


def simple_text_summary(df: pd.DataFrame):
    """Produce a short human-readable summary from the DataFrame."""
    ana = analyze_jobs(df)
    total = ana.get("total_jobs", 0)
    top = ana.get("top_skills", [])[:5]
    skills_list = ", ".join([s["skill"] for s in top]) if top else "(none)"
    sal = ana.get("salary", {})
    mean = sal.get("mean")
    if mean is not None:
        mean_str = f"${mean:,.0f}"
    else:
        mean_str = "N/A"

    return f"Analyzed {total} jobs. Top skills: {skills_list}. Average salary (where available): {mean_str}."


def ai_summary_gemini(df: pd.DataFrame, api_key: str = None, prompt: str = None) -> str:
    """Generate an AI-powered summary using Google Gemini API.
    
    Args:
        df: jobs DataFrame
        api_key: Google Gemini API key (optional; can also use env var GEMINI_API_KEY)
        prompt: custom prompt; if None, uses a default
    
    Returns:
        AI-generated summary string
    
    Requires: pip install google-generativeai
    Set GEMINI_API_KEY environment variable or pass api_key param.
    """
    import os
    
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "Gemini API key not configured. Set GEMINI_API_KEY environment variable."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    except ImportError:
        return "google-generativeai not installed. Run: pip install google-generativeai"
    
    # Prepare context from analysis
    ana = analyze_jobs(df)
    top_skills = ana.get("top_skills", [])[:10]
    skills_text = ", ".join([s["skill"] for s in top_skills])
    salary = ana.get("salary", {})
    
    if prompt is None:
        prompt = f"""
        Based on the job market analysis below, provide a concise AI career insights summary (2-3 sentences max):
        
        Total Jobs Analyzed: {len(df)}
        Top Skills in Demand: {skills_text}
        Average Salary: ${salary.get('mean', 'N/A'):,.0f}
        Salary Range: ${salary.get('min', 'N/A'):,.0f} - ${salary.get('max', 'N/A'):,.0f}
        
        Focus on actionable career advice and market trends.
        """
    
    last_error = None
    for model_name in _GEMINI_MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = _extract_gemini_text(response)
            if text:
                return text
            last_error = f"Gemini API returned an empty response for {model_name}."
        except Exception as exc:  # pragma: no cover - depends on API state
            error_text = str(exc)
            last_error = f"{model_name}: {error_text}"
            # For 404/not found, move to the next candidate automatically.
            if "404" in error_text or "not found" in error_text.lower():
                continue
            return f"Gemini API error: {error_text}"

    return f"Gemini API error: {last_error or 'No models produced a response.'}"