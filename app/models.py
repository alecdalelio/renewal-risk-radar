"""
Pydantic models for the Renewal Risk Radar application.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class AnalyzeRequest(BaseModel):
    """Request model for contract analysis."""
    # TODO: Add full schema as requirements are defined
    contract_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AnalyzeResponse(BaseModel):
    """Response model for contract analysis."""
    # TODO: Add full schema as requirements are defined
    risk_score: Optional[float] = None
    analysis: Optional[Dict[str, Any]] = None
