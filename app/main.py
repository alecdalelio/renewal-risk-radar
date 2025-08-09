"""
Renewal Risk Radar FastAPI Application

Main FastAPI application for the Renewal Risk Radar MVP.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Renewal Risk Radar",
    description="AI-powered contract renewal risk analysis",
    version="0.1.0",
)


@app.get("/healthz")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
