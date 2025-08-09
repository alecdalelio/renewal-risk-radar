# Renewal Risk Radar

**FastAPI project that analyzes customer usage and support signals to predict renewal risk and recommend GTM actions.**

Renewal Risk Radar ingests account-level product usage, support tickets, and customer notes, then produces:
- A **renewal risk score** (0–100) with top risk drivers and supporting evidence
- **Expansion opportunities** inferred from usage patterns
- A prioritized **playbook** of recommended actions
- Ready-to-use internal Slack and customer email drafts

## 🚀 Tech Stack
- **FastAPI** for API routes
- **Pydantic v2** for request/response validation
- **SQLite** (planned) for persistence and caching
- **Ruff** + **Black** + **pre-commit** for linting and formatting

## 📂 Project Structure
```
renewal-risk-radar/
├── app/
│   ├── main.py          # API routes
│   ├── models.py        # Request/response schemas
│   ├── features.py      # Feature extraction from raw data
│   ├── reasoner.py      # Risk scoring + playbook generation
│   ├── redact.py        # PII scrubbing
│   ├── store.py         # Persistence (to be implemented)
│   └── config.py        # Env settings
├── tests/               # Pytest suite
├── data/                # Sample CSV + notes
├── scripts/             # Utility scripts
└── docs/                # Spec + design notes
```

## 🛠 Setup
1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd renewal-risk-radar
   ```
2. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install pre-commit && pre-commit install
   ```
3. **Run tests**
   ```bash
   make test
   ```
4. **Start the dev server**
   ```bash
   make run
   ```
   Visit `http://localhost:8000/docs` for interactive API docs.

## 📡 Example Usage
**Health check**
```bash
curl -s http://localhost:8000/healthz
# {"status": "ok"}
```

**(Planned in Phase 2)** Scoring an account with sample data:
```bash
curl -s -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{"account_id":"ACME_CORP"}'
```

## 📅 Development Phases
- **Phase 1 (✅)** Scaffold project, `/healthz` route, tests, tooling
- **Phase 2** Implement `/score`, ingest sample data, return hardcoded but schema-valid JSON
- **Phase 3** Integrate LLM with strict JSON output + validation/repair pass
- **Phase 4** Add persistence, caching, and metrics
- **Phase 5** Lightweight evals + reporting
- **Phase 6** Deploy (Render/Railway) + optional Slack/CRM integrations

---

**Status:** In active development — currently private, will be made public after polish.
