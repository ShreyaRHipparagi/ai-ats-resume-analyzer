# 🧠 AI Career Architect — Resume & Career Intelligence

[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-blue?logo=google-gemini)](https://aistudio.google.com/app/apikey) [![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)](https://flask.palletsprojects.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Career Architect is an intelligent, end-to-end resume and career coaching assistant built to help students and early-career professionals escape the "black hole" of automated rejections and enter the interview funnel with confidence. Designed for hackathons and rapid iteration, the system combines high-fidelity PDF parsing with a multi-agent AI backbone (Google Gemini) to deliver actionable, prioritized guidance and a personalized learning roadmap.

Table of contents
- Problem
- Solution overview
- Key features
- Architecture & data flow
- Scoring & output format
- Installation & development setup
- Usage (CLI / API / Example)
- Deployment
- Security & privacy
- Testing & CI
- Roadmap
- Contributing
- License & credits
- Contact

---

## 🔴 Problem statement — "The Black Hole of Applications"
Many applicants—especially students and early-career professionals—submit dozens or hundreds of applications and are rejected automatically by Applicant Tracking Systems (ATS) without feedback. Typical pain points:
- No clear signal why an application failed
- Random resume edits hoping to match job descriptions (inefficient)
- Decreasing motivation after repeated rejections
- No structured plan to close real skill gaps

---

## ✨ Solution overview
AI Career Architect performs multi-perspective analysis of a resume against a target job description (JD) using three complementary personas:
1. ATS Simulator — scores keyword & skill matches and identifies formatting issues.
2. Cynical Senior Recruiter — provides candid, recruiter-style feedback and prioritised actions.
3. FAANG Mentor — rewrites bullets using an impact-first formula (Google X-Y-Z) and designs a 6-month learning roadmap.

Outcomes:
- Deterministic, JSON-first outputs for consistent UI rendering
- Prioritised, actionable improvements to resume and skill set
- Rewritten bullets and templates tuned for recruiter and FAANG expectations

---

## 🏷️ Key features
- ATS Score Breakdown: granular scoring (keywords, skills, experience, format, actionability)
- Recruiter Feedback: specific, prioritized reasons for rejection or shortlisting
- FAANG-Style Rewrites: impact-first bullet rewrites (metrics, what-you-did, outcome)
- Personalized 6‑Month Roadmap: milestones, goals, and curated learning resources
- Robust PDF parsing: high-fidelity text extraction using PyMuPDF
- Deterministic outputs: JSON schema via `response_mime_type: application/json` for each agent

---

## 🏗️ Architecture & flow

```mermaid
graph TD
    User([User]) -->|Upload PDF + Job Description| Flask[Flask App]
    Flask -->|PDF Extraction| PyMuPDF[PyMuPDF Engine]
    PyMuPDF -->|Clean Text| GeminiAgent[Gemini Multi-Agent System]

    subgraph Gemini Intelligence
        GeminiAgent -->|Role 1| ATS[ATS Simulator]
        GeminiAgent -->|Role 2| Recruiter[Senior Recruiter]
        GeminiAgent -->|Role 3| Mentor[FAANG Mentor]
    end

    ATS -->|JSON Output| Dashboard[Premium Dashboard]
    Recruiter -->|JSON Output| Dashboard
    Mentor -->|JSON Output| Dashboard

    Dashboard -->|Actionable Value| User
```

High level flow:
1. User uploads resume PDF and a target job description.
2. Backend extracts and normalises text (PyMuPDF) and prepares structured prompts.
3. Multi-agent Gemini system (ATS, Recruiter, Mentor) returns deterministic JSON payloads.
4. Frontend/dashboard consumes JSON and renders prioritized actions, rewrites, and a learning roadmap.

---

## 🔬 Scoring methodology (high level)
The scoring engine composes a final ATS score from weighted components:

- Keyword match — 30%: exact matches, stemming, synonyms and context-aware embeddings
- Skills & tools relevance — 25%: domain/tool weighting based on JD
- Experience fit — 25%: seniority, role-specific responsibilities, quantifiable achievements
- Format & readability — 10%: section structure, headings, contact info, font/layout issues detected from PDF
- Actionability — 10%: presence of metrics, results-oriented language

Each category produces a sub-score and the engine emits the combined ATS score plus supporting data such as matched keywords, missed high-priority items, and suggestions.

---

## 📦 Output format (example)
All agents return structured JSON for predictable UI rendering. Example (abbreviated):

```json
{
  "ats": {
    "score": 62,
    "breakdown": {
      "keywords": 70,
      "skills": 55,
      "experience": 60,
      "format": 90,
      "actionability": 30
    },
    "matched_keywords": ["react", "nodejs", "rest api"],
    "missing_high_priority_skills": ["system design", "scalability"]
  },
  "recruiter_feedback": {
    "summary": "Resume shows strong frontend experience but lacks scale and leadership examples.",
    "detailed": [
      "Bullets are task-focused; emphasise outcomes and metrics.",
      "Add backend integration projects showing design decisions and measurable impact."
    ],
    "priority_actions": [
      {"id": "P1", "text": "Rewrite bullets to include metrics", "impact": "high"}
    ]
  },
  "mentor_rewrites": [
    {
      "original": "Worked on a web app with React",
      "rewrite": "Led development of a React-based web application used by 10k+ monthly users; reduced page load time by 40% via code-splitting and lazy-loading."
    }
  ],
  "learning_plan": {
    "horizon_months": 6,
    "milestones": [
      {"month": 1, "goal": "Core system design concepts"},
      {"month": 3, "goal": "Build and deploy a full-stack project with metrics"}
    ],
    "resources": [
      {"title": "System Design Primer", "url": "https://example.com"}
    ]
  }
}
```

Refer to docs/openapi.yaml (planned) for the full schema.

---

## 🚀 Installation & Quickstart

Prerequisites
- Python 3.10+
- pip
- (Optional) virtualenv / venv
- Google Gemini API access (or compatible LLM endpoint) and API key

1. Clone the repository
```bash
git clone https://github.com/ShreyaRHipparagi/ai-ats-resume-analyzer.git
cd ai-ats-resume-analyzer
```

2. Create virtual environment and install
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3. Environment variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_APP=main.py
DEBUG=true
```

4. Run the application (development)
```bash
python main.py
```
By default the Flask backend serves API endpoints documented below.

---

## 🧭 API endpoints (example)

- POST /api/analyze
  - Payload: multipart/form-data or JSON
    - resume: PDF file (multipart) OR resume_text (string)
    - job_description: text
    - options: { "model": "gemini-1.5-flash", "strict_mode": true }
  - Response: JSON payload containing ATS score, recruiter feedback, mentor rewrites, and learning plan

- GET /api/status
  - Health check for service and LLM connectivity

Example cURL (resume file upload):
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=$(< job_description.txt)"
```

Example JSON payload (resume_text mode):
```json
{
  "resume_text": "Jane Doe — Software Engineer. Built web apps using React and Node.js...",
  "job_description": "We are hiring a Full-Stack Engineer with React and Node experience...",
  "options": { "model": "gemini-1.5-flash", "strict_mode": false }
}
```

---

## 📦 Docker & production notes
A production deployment should run the Flask app behind a WSGI server (e.g., Gunicorn) and expose a secure HTTPS endpoint. Example Dockerfile (simplified):

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app", "--workers", "4"]
```

Recommendations:
- Use managed secrets (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager)
- Rate-limit and queue LLM calls to avoid spikes and cost overruns
- Cache repeated JD/resume comparisons for faster results
- Implement file retention policies (auto-delete or user opt-in persistance)
- Monitor LLM call costs and offer user-facing usage quotas for paid tiers

---

## 🛡️ Privacy & Security
- Treat uploaded resumes as sensitive personal data:
  - Encrypt data at rest (AES-256) and in transit (HTTPS/TLS)
  - Offer clear retention and deletion controls
  - Log minimally and redact PII in debug logs
- When using third-party LLMs, ensure contractual data protection and consider on-prem or private LLM deployments for heightened privacy.

---

## ✅ Testing & CI
- Unit tests for parsing, normalization, scoring, and JSON schema validation
- Integration tests that mock LLM responses for deterministic checks
- E2E smoke tests for the API contract

Example GitHub Actions workflow (CI):

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
      - name: Lint
        run: |
          source .venv/bin/activate
          pip install flake8 black
          flake8 .
      - name: Run tests
        run: |
          source .venv/bin/activate
          pip install -r requirements.txt
          pytest -q
      - name: Dependency scan
        run: |
          pip install pip-audit
          pip-audit --progress
```

Add secrets for test coverage and code scanning as needed.

---

## 🔭 Roadmap & future scope
Planned enhancements:
- LinkedIn Deep-Sync: adapt profile sections and headlines automatically
- Mock Interview AI: timed, voice-enabled interview practice with feedback
- Multi-lingual analysis and localized JD parsing
- Recruiter dashboard for enterprise customers and ATS integrations
- Offline/local LLM support (self-hosted models) for privacy-sensitive deployments
- OpenAPI/Swagger documentation and SDKs (Python/JS)

---

## 🧩 Extensibility & integration points
- Replace or extend the LLM backend by implementing an adapter interface
- Add personas/agents (Hiring Manager, Diversity & Inclusion reviewer)
- Integrate with ATS vendors or job platforms for direct application submission
- Export rewritten resumes to common templates (PDF, DOCX) with confidence checks

---

## 👩‍💻 Contributing
Contributions welcome! Suggested workflow:
1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Add tests and documentation
4. Open a pull request with a clear description and rationale

Please follow the code style (Black + Flake8) and include tests for significant changes. See CONTRIBUTING.md for detailed contributor guidelines (add this file if absent).

---

## 📝 License
MIT © 2026 AI Career Architect — Shreya R. Hipparagi  
Repository: https://github.com/ShreyaRHipparagi/ai-ats-resume-analyzer

---

## Credits
- Built with Google Gemini (LLM)
- PyMuPDF for PDF parsing
- Flask for the API backend
- Project scaffold inspired by community best-practices for secure AI services

---

## Contact
Project maintainer: Shreya R. Hipparagi  
Repository: https://github.com/ShreyaRHipparagi/ai-ats-resume-analyzer  
For questions, feature requests, or enterprise inquiries, open an issue or send an email (add contact email in repo settings).

---

If you'd like, I can:
- produce an OpenAPI (Swagger) spec for the API endpoints,
- add example unit tests and CI workflow files to the repository,
- generate a sample dashboard JSON-to-UI mapping or a minimal React demo,
- or prepare a Docker Compose + production deployment guide.

Tell me which of the above you'd like next and I'll prepare the files.
