"""
Renewal Risk Radar FastAPI Application

Main FastAPI application for the Renewal Risk Radar MVP.
"""

from fastapi import FastAPI, HTTPException
from .models import AnalyzeRequest, AnalyzeResponse
from . import redact, features, reasoner
import csv
from pathlib import Path

app = FastAPI(
    title="Renewal Risk Radar",
    description="AI-powered contract renewal risk analysis",
    version="0.2.0",
)


@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


def _load_csv(path: Path) -> list[dict]:
    """Load CSV file and return list of dictionaries."""
    with path.open() as f:
        return list(csv.DictReader(f))


@app.post("/score", response_model=AnalyzeResponse)
async def score(req: AnalyzeRequest):
    """Score account renewal risk and generate recommendations."""
    data_dir = Path("data")

    # Load data from request or sample files
    usage_rows = req.usage or (
        _load_csv(data_dir / "usage_sample.csv") 
        if (data_dir / "usage_sample.csv").exists() 
        else None
    )
    tickets_rows = req.tickets or (
        _load_csv(data_dir / "tickets_sample.csv") 
        if (data_dir / "tickets_sample.csv").exists() 
        else None
    )
    notes_text = (
        req.notes 
        if req.notes is not None 
        else (
            (data_dir / "notes_sample.md").read_text() 
            if (data_dir / "notes_sample.md").exists() 
            else ""
        )
    )

    if usage_rows is None or tickets_rows is None:
        raise HTTPException(
            status_code=400, 
            detail="Missing usage/tickets and sample files not found"
        )

    # Process data through pipeline
    redacted = redact.redact_sensitive_data(notes_text or "")
    feats = features.compute_features(usage_rows, tickets_rows, redacted)
    snippets = [
        line.strip() 
        for line in (redacted.splitlines()[:2] if redacted else []) 
        if line.strip()
    ]

    return reasoner.score_account(
        features=feats, 
        snippets=snippets, 
        account_id=req.account_id
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)