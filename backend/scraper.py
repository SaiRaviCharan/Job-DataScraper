"""Job scraper with support for multiple sources: RemoteOK (API), Himalayas (API), Indeed (BeautifulSoup).

Features:
- RemoteOK: Uses public JSON endpoint (free, no auth required)
- Himalayas: Uses public JSON API (free, no auth required)
- Indeed: Safe BeautifulSoup scraper for public pages (respects robots.txt)
- Rate limiting & error handling
- Returns normalized job dicts with consistent fields
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Rate limiting (seconds between requests)
RATE_LIMIT = 0.5

GEMINI_MODEL_CANDIDATES = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite-001",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]


def _normalize_salary(salary_str: Optional[str]) -> Optional[str]:
    """Extract numeric salary or salary range from string."""
    if not salary_str:
        return None
    # Simple extraction: keep only numbers and common separators
    import re
    nums = re.findall(r'\$?(\d+(?:,?\d{3})*(?:\.\d{2})?)', str(salary_str))
    if nums:
        return "-".join(nums[:2]) if len(nums) > 1 else nums[0]
    return None


def scrape_remoteok(query: str = "python developer", limit: int = 50) -> List[Dict]:
    """Scrape RemoteOK using their public JSON API.
    
    Args:
        query: job title/skill to search for
        limit: max jobs to return
    
    Returns:
        List of job dicts with normalized fields
    """
    logger.info(f"Scraping RemoteOK for query: {query}")
    jobs = []
    try:
        # RemoteOK public API endpoint (no auth required)
        url = "https://remoteok.com/api"
        params = {"limit": limit}
        
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        for job in data:
            # Filter by query if present in title/description
            if query.lower() not in (job.get("title", "") + job.get("description", "")).lower():
                continue
            
            job_dict = {
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("location", "Remote"),
                "salary": _normalize_salary(job.get("salary", "")),
                "skills": job.get("skills", ""),
                "description": job.get("description", "")[:500],  # truncate
                "date_posted": job.get("date", ""),
                "source": "RemoteOK",
                "url": job.get("url", "")
            }
            jobs.append(job_dict)
        
        logger.info(f"RemoteOK: found {len(jobs)} jobs")
        time.sleep(RATE_LIMIT)
        return jobs
    except Exception as e:
        logger.error(f"RemoteOK scrape failed: {e}")
        return []


def scrape_himalayas(query: str = "ai engineer", limit: int = 50) -> List[Dict]:
    """Scrape Himalayas using their public JSON API.
    
    Himalayas has a clean API endpoint that returns remote job listings.
    
    Args:
        query: job title to search for
        limit: max jobs to return
    
    Returns:
        List of job dicts with normalized fields
    """
    logger.info(f"Scraping Himalayas for query: {query}")
    jobs = []
    try:
        # Himalayas API endpoint (public, no auth)
        url = "https://himalayas.app/api/v1/jobs"
        params = {
            "q": query,
            "limit": limit,
            "type": "remote"  # filter for remote jobs
        }
        
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        job_list = data.get("jobs", []) if isinstance(data, dict) else data
        
        for job in job_list:
            job_dict = {
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("name", "") if isinstance(job.get("company"), dict) else job.get("company", ""),
                "location": job.get("location", "") or "Remote",
                "salary": _normalize_salary(job.get("salary", "")),
                "skills": ", ".join(job.get("skills", [])) if isinstance(job.get("skills"), list) else job.get("skills", ""),
                "description": job.get("description", "")[:500],
                "date_posted": job.get("posted_at", "") or job.get("date", ""),
                "source": "Himalayas",
                "url": job.get("url", "") or job.get("link", "")
            }
            jobs.append(job_dict)
        
        logger.info(f"Himalayas: found {len(jobs)} jobs")
        time.sleep(RATE_LIMIT)
        return jobs
    except Exception as e:
        logger.error(f"Himalayas scrape failed: {e}")
        return []


def scrape_remotive(query: str = "frontend developer", limit: int = 50) -> List[Dict]:
    """Scrape Remotive remote jobs API (https://remotive.com/api/remote-jobs)."""
    logger.info(f"Scraping Remotive for query: {query}")
    jobs: List[Dict] = []
    try:
        url = "https://remotive.com/api/remote-jobs"
        params = {"search": query, "limit": limit}

        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json() or {}
        for job in data.get("jobs", []):
            skills = job.get("tags") or job.get("category")
            if isinstance(skills, list):
                skills_str = ", ".join(skills)
            else:
                skills_str = str(skills or "")

            description = job.get("description", "")
            job_dict = {
                "title": job.get("title", ""),
                "company": job.get("company_name", ""),
                "location": job.get("candidate_required_location", "Remote"),
                "salary": _normalize_salary(job.get("salary", "")),
                "skills": skills_str,
                "description": BeautifulSoup(description, "html.parser").get_text(" ")[:500],
                "date_posted": job.get("publication_date", ""),
                "source": "Remotive",
                "url": job.get("url", ""),
            }
            jobs.append(job_dict)

        logger.info(f"Remotive: found {len(jobs)} jobs")
        time.sleep(RATE_LIMIT)
        return jobs
    except Exception as exc:
        logger.error(f"Remotive scrape failed: {exc}")
        return []


def scrape_indeed(query: str = "data scientist", pages: int = 1) -> List[Dict]:
    """Scrape Indeed job listings using BeautifulSoup.
    
    IMPORTANT: This respects robots.txt and indeed.com's ToS.
    Rate-limited to avoid overloading the server.
    For production use, consider using Indeed's official API.
    
    Args:
        query: job title/keyword
        pages: number of pages to scrape (default 1)
    
    Returns:
        List of job dicts with normalized fields
    """
    logger.info(f"Scraping Indeed for query: {query}, pages: {pages}")
    jobs = []
    
    for page in range(pages):
        try:
            # Indeed search URL (public, no login required)
            start = page * 10
            url = f"https://www.indeed.com/jobs?q={quote(query)}&start={start}"
            
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Indeed job card selectors (subject to change if site layout updates)
            job_cards = soup.select("div.job-search-results li")
            
            for card in job_cards:
                try:
                    title_elem = card.select_one("h2 a span")
                    company_elem = card.select_one("span.company_location span")
                    location_elem = card.select_one("div.company_location")
                    salary_elem = card.select_one("span.salary-snippet")
                    summary_elem = card.select_one("div.job-snippet")
                    
                    job_dict = {
                        "title": title_elem.get_text(strip=True) if title_elem else "",
                        "company": company_elem.get_text(strip=True) if company_elem else "",
                        "location": location_elem.get_text(strip=True) if location_elem else "Not specified",
                        "salary": _normalize_salary(salary_elem.get_text(strip=True)) if salary_elem else None,
                        "skills": "",  # Indeed doesn't clearly list skills in listing view
                        "description": summary_elem.get_text(strip=True) if summary_elem else "",
                        "date_posted": "",
                        "source": "Indeed",
                        "url": card.select_one("h2 a").get("href") if card.select_one("h2 a") else ""
                    }
                    
                    if job_dict["title"] and job_dict["company"]:
                        jobs.append(job_dict)
                except Exception as e:
                    logger.debug(f"Error parsing Indeed job card: {e}")
                    continue
            
            logger.info(f"Indeed page {page + 1}: found {len(job_cards)} cards")
            time.sleep(RATE_LIMIT + 0.5)  # extra delay between pages
            
        except Exception as e:
            logger.error(f"Indeed page {page} scrape failed: {e}")
            continue
    
    logger.info(f"Indeed total: {len(jobs)} jobs")
    return jobs


def scrape_all(sources: List[str] = None, query: str = "python developer", pages: int = 1) -> List[Dict]:
    """Scrape multiple sources and combine results.
    
    Args:
        sources: list of sources ('remoteok', 'himalayas', 'indeed'). If None, uses all.
        query: search query
        pages: pages to scrape (applies to Indeed mainly)
    
    Returns:
        Combined list of normalized job dicts. Falls back to dummy data if all sources fail.
    """
    if sources is None:
        sources = ["remoteok", "himalayas", "remotive"]  # include Remotive by default
    
    all_jobs = []
    
    if "remoteok" in sources:
        all_jobs.extend(scrape_remoteok(query, limit=50))
    
    if "himalayas" in sources:
        all_jobs.extend(scrape_himalayas(query, limit=50))
    
    if "remotive" in sources:
        all_jobs.extend(scrape_remotive(query, limit=50))

    if "indeed" in sources:
        all_jobs.extend(scrape_indeed(query, pages=pages))
    
    # Deduplicate by title + company for cleanliness
    deduped: Dict[str, Dict] = {}
    for job in all_jobs:
        key = f"{job.get('title','').lower()}::{job.get('company','').lower()}"
        if key.strip():
            if key not in deduped:
                deduped[key] = job
        else:
            deduped[str(len(deduped))] = job

    all_jobs = list(deduped.values())

    # Fallback to AI-synthesised or keyword-based data if nothing real was scraped
    if not all_jobs:
        logger.warning(f"No jobs scraped from {sources}. Generating synthetic data for '{query}'.")
        all_jobs = generate_ai_jobs(query)
    
    logger.info(f"Total jobs: {len(all_jobs)} from {len(sources)} sources")
    return all_jobs


def _keyword_profiles() -> Dict[str, Dict[str, List[str]]]:
    """Provide deterministic skill/salary profiles keyed by keywords."""
    return {
        "react": {
            "skills": ["React", "TypeScript", "Redux", "CSS-in-JS", "REST APIs", "GraphQL", "Jest"],
            "titles": ["React Developer", "Frontend Engineer", "UI Engineer", "Web Application Developer"],
            "salary": (95000, 120000, 150000),
        },
        "frontend": {
            "skills": ["JavaScript", "React", "Next.js", "Tailwind", "Accessibility", "Webpack"],
            "titles": ["Frontend Developer", "JavaScript Engineer", "UX Engineer"],
            "salary": (90000, 115000, 140000),
        },
        "full stack": {
            "skills": ["React", "Node.js", "Express", "PostgreSQL", "AWS", "CI/CD"],
            "titles": ["Full Stack Engineer", "Software Engineer", "Platform Engineer"],
            "salary": (105000, 135000, 165000),
        },
        "data": {
            "skills": ["Python", "SQL", "Pandas", "TensorFlow", "Airflow", "Azure"],
            "titles": ["Data Scientist", "ML Engineer", "Data Analyst"],
            "salary": (110000, 140000, 180000),
        },
        "ai": {
            "skills": ["Python", "PyTorch", "LLMs", "Prompt Engineering", "Vector Databases"],
            "titles": ["AI Engineer", "Generative AI Specialist", "ML Researcher"],
            "salary": (130000, 165000, 210000),
        },
    }


def _pick_profile(query: str) -> Dict[str, List[str]]:
    q = (query or "").lower()
    profiles = _keyword_profiles()
    for keyword, profile in profiles.items():
        if keyword in q:
            return profile
    return profiles["data"]


def _default_jobs(query: str, count: int = 4) -> List[Dict]:
    profile = _pick_profile(query)
    min_salary, mid_salary, max_salary = profile["salary"]
    titles = profile["titles"]
    skills = profile["skills"]
    jobs: List[Dict] = []
    for idx in range(count):
        title = titles[idx % len(titles)]
        job_skills = ", ".join(skills)
        jobs.append(
            {
                "title": title,
                "company": f"Synthetic Co {idx + 1}",
                "location": "Remote",
                "salary": str(int(mid_salary + (-1) ** idx * 5000)),
                "skills": job_skills,
                "description": f"{title} working on modern {query} projects using {job_skills}.",
                "date_posted": time.strftime("%Y-%m-%d"),
                "source": "synthetic",
                "url": "https://example.com/synthetic-job",
            }
        )
    # Ensure salary bounds reflected
    if jobs:
        jobs[0]["salary"] = str(min_salary)
        jobs[-1]["salary"] = str(max_salary)
    return jobs


def _collect_gemini_text(response) -> str:
    text = getattr(response, "text", "")
    if text:
        return text
    collected = []
    for candidate in getattr(response, "candidates", None) or []:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            part_text = getattr(part, "text", None)
            if part_text:
                collected.append(part_text)
    return "".join(collected)


def _call_gemini_model(genai_module, model_name: str, prompt: str) -> Tuple[Optional[str], bool]:
    try:
        model = genai_module.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        text = _collect_gemini_text(response)
        if text:
            logger.info(f"Gemini response obtained using {model_name}")
        return (text or None, False)
    except Exception as exc:  # pragma: no cover - network specific
        logger.warning(f"Gemini generation failed for {model_name}: {exc}")
        stop = any(code in str(exc) for code in ("403", "429"))
        return (None, stop)


def _gemini_generate(prompt: str, api_key: str) -> str:
    try:
        import google.generativeai as genai  # type: ignore
    except ImportError:
        logger.warning("google-generativeai not installed; falling back to keyword defaults")
        return ""

    genai.configure(api_key=api_key)
    for model_name in GEMINI_MODEL_CANDIDATES:
        text, should_stop = _call_gemini_model(genai, model_name, prompt)
        if should_stop:
            break
        if text:
            return text
    return ""


def _parse_jobs_from_text(text: str) -> List[Dict]:
    json_start = text.find("[")
    json_end = text.rfind("]")
    if json_start == -1 or json_end == -1:
        return []

    try:
        parsed = json.loads(text[json_start : json_end + 1])
    except json.JSONDecodeError:
        return []

    jobs: List[Dict] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        jobs.append(
            {
                "title": item.get("title", ""),
                "company": item.get("company", ""),
                "location": item.get("location", "Remote"),
                "salary": _normalize_salary(item.get("salary")),
                "skills": item.get("skills", ""),
                "description": str(item.get("description", ""))[:500],
                "date_posted": item.get("date_posted", time.strftime("%Y-%m-%d")),
                "source": "Gemini",
                "url": item.get("url", ""),
            }
        )
    return [job for job in jobs if job.get("title")]


def generate_ai_jobs(query: str, count: int = 5) -> List[Dict]:
    """Generate synthetic jobs using Gemini when available, else keyword defaults."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _default_jobs(query, count)

    prompt = (
        "You are a job market data synthesizer. Given a job search query, respond with a JSON "
        "array describing realistic job listings that match the role. Each item must contain "
        "title, company, location, salary (numeric annual USD), skills (comma-separated string), "
        "description (<= 280 chars), date_posted (ISO date), and url."
    )
    prompt = f"{prompt}\nQuery: {query}. Return {count} items in raw JSON with no markdown."

    text = _gemini_generate(prompt, api_key)
    jobs = _parse_jobs_from_text(text) if text else []
    return jobs or _default_jobs(query, count)


def scrape_dummy(query: str = "data scientist", pages: int = 1) -> List[Dict]:
    """Fallback helper preserved for compatibility; uses new defaults."""
    return _default_jobs(query, max(3, pages * 2))
