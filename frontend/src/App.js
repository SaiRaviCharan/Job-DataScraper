import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scraping, setScraping] = useState(false);
  const [query, setQuery] = useState('python developer');
  const [useAI, setUseAI] = useState(false);
  const [toast, setToast] = useState(null);

  const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000';

  useEffect(() => {
    fetchAnalysis();
  }, []);

  useEffect(() => {
    if (!toast) return;
    const timeout = setTimeout(() => setToast(null), 4000);
    return () => clearTimeout(timeout);
  }, [toast]);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/analysis`);
      if (!res.ok) throw new Error('Failed to fetch analysis');
      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async (useGemini = false) => {
    try {
      const res = await fetch(`${API_BASE}/api/summary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ use_ai: useGemini })
      });
      if (!res.ok) throw new Error('Failed to fetch summary');
      const data = await res.json();
      setSummary(data.summary);
      setUseAI(useGemini);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleScrape = async () => {
    setScraping(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/scrape`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query,
          sources: ['remoteok', 'himalayas', 'remotive'],
          pages: 1
        })
      });
      if (!res.ok) throw new Error('Scrape failed');
      const data = await res.json();
      const status = data.status || 'ok';
      const message =
        data.message ||
        (status === 'warning'
          ? 'No jobs were found for this search.'
          : `Scraped ${data.count || 0} jobs.`);
      setToast({ status, message });
      fetchAnalysis();
      fetchSummary(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setScraping(false);
    }
  };

  const handleSummaryClick = (mode) => {
    setToast(null);
    fetchSummary(mode);
  };

  if (loading) {
    return (
      <div className="app-shell">
        <div className="ambient" />
        <div className="loading">Loading job market analysis...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-shell">
        <div className="ambient" />
        <div className="error">
          <h2>Something went wrong</h2>
          <p>{error}</p>
          <p style={{ fontSize: '0.9em', color: 'rgba(148, 163, 184, 0.8)' }}>
            Ensure the Flask backend is running on http://localhost:5000 and retry.
          </p>
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="app-shell">
        <div className="ambient" />
        <div className="error">
          <h2>No data yet</h2>
          <p>Use the scraper to ingest roles and unlock analytics.</p>
        </div>
      </div>
    );
  }

  const salary = analysis.salary || {};

  return (
    <div className="app-shell">
      <div className="ambient" />
      {toast && (
        <div className={`toast toast-${toast.status}`}>
          <span>{toast.message}</span>
        </div>
      )}
      <main className="content">
        <header className="hero">
          <div className="hero-text">
            <p className="eyebrow">Live labour market telemetry</p>
            <h1>Job Market Insights</h1>
            <p className="subtitle">
              Track salary trends, skill demand, and AI-curated summaries for any role in seconds.
            </p>
          </div>
          <div className="hero-metric">
            <span className="metric-label">Jobs analysed</span>
            <span className="metric-value">{analysis.total_jobs}</span>
          </div>
        </header>

        <section className="card scraper-card">
          <div className="card-header">
            <h2>Scrape fresh openings</h2>
            <p>Query multiple remote job boards and refresh analytics instantly.</p>
          </div>
          <div className="scraper-form">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Try 'React developer', 'AI engineer', ..."
              className="input"
            />
            <button
              onClick={handleScrape}
              disabled={scraping}
              className="btn btn-primary"
            >
              {scraping ? 'Scraping…' : '⚡ Scrape Jobs'}
            </button>
          </div>
        </section>

        <section className="card metrics-card">
          <div className="card-header">
            <h2>Market overview</h2>
            <p>A snapshot of the current dataset pulled from the latest scrape.</p>
          </div>
          <div className="metric-grid">
            <div className="metric-card">
              <span className="metric-title">Total roles</span>
              <span className="metric-number">{analysis.total_jobs}</span>
            </div>
            <div className="metric-card">
              <span className="metric-title">Average salary</span>
              <span className="metric-number">
                {salary.mean ? `$${(salary.mean / 1000).toFixed(0)}k` : 'N/A'}
              </span>
            </div>
            <div className="metric-card">
              <span className="metric-title">Floor salary</span>
              <span className="metric-number">
                {salary.min ? `$${(salary.min / 1000).toFixed(0)}k` : 'N/A'}
              </span>
            </div>
            <div className="metric-card">
              <span className="metric-title">Ceiling salary</span>
              <span className="metric-number">
                {salary.max ? `$${(salary.max / 1000).toFixed(0)}k` : 'N/A'}
              </span>
            </div>
          </div>
        </section>

        <div className="insight-grid">
          <section className="card skills-card">
            <div className="card-header">
              <h2>In-demand stack</h2>
              <p>Skill frequency based on current listings.</p>
            </div>
            <div className="skills-list">
              {analysis.top_skills && analysis.top_skills.length > 0 ? (
                analysis.top_skills.slice(0, 15).map((skill, idx) => (
                  <div key={idx} className="skill-item">
                    <div className="skill-meta">
                      <span className="skill-rank">#{idx + 1}</span>
                      <span className="skill-name">{skill.skill}</span>
                    </div>
                    <div className="skill-progress">
                      <div
                        className="skill-progress-fill"
                        style={{
                          width: `${(skill.count / analysis.top_skills[0].count) * 100}%`
                        }}
                      />
                    </div>
                    <span className="skill-count">{skill.count}</span>
                  </div>
                ))
              ) : (
                <p className="placeholder">No skills data available yet.</p>
              )}
            </div>
          </section>

          <section className="card summary-card">
            <div className="card-header">
              <h2>Career narrative</h2>
              <p>
                {useAI
                  ? 'AI generated guidance powered by Gemini Flash.'
                  : 'Quick human-readable snapshot of the dataset.'}
              </p>
            </div>
            <div className="summary-area">
              {summary ? (
                <p className="summary-text">{summary}</p>
              ) : (
                <p className="placeholder">Generate insights to see intelligence here.</p>
              )}
            </div>
            <div className="summary-actions">
              <button
                onClick={() => handleSummaryClick(false)}
                className={`btn btn-ghost ${!useAI ? 'active' : ''}`}
              >
                📝 Simple summary
              </button>
              <button
                onClick={() => handleSummaryClick(true)}
                className={`btn btn-ghost ${useAI ? 'active' : ''}`}
              >
                ✨ Gemini summary
              </button>
            </div>
          </section>
        </div>

        <section className="card footer-card">
          <div className="footer-grid">
            <div>
              <h3>Data vendors</h3>
              <p>RemoteOK · Himalayas · Indeed (HTML fallback)</p>
            </div>
            <div>
              <h3>API endpoint</h3>
              <p>{API_BASE}</p>
            </div>
            <div>
              <h3>Gemini model</h3>
              <p>{useAI ? 'Gemini 2.0 Flash (free tier)' : 'Not in use'}</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
