"""
Pydantic models for the Renewal Risk Radar application.
"""

from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request model for contract analysis."""
    account_id: str
    usage: Optional[List[Dict[str, Any]]] = None
    tickets: Optional[List[Dict[str, Any]]] = None
    notes: Optional[str] = None


class RiskDriver(BaseModel):
    """Individual risk factor with weight and explanation."""
    signal: str
    weight: float = Field(ge=0, le=1)
    explanation: str


class PlaybookItem(BaseModel):
    """Recommended action with owner and timeline."""
    owner: Literal["CSM", "Sales", "Solutions", "RevOps", "Support"]
    action: str
    eta_days: int


class Comms(BaseModel):
    """Ready-to-use communication templates."""
    internal_slack: str
    client_email: str


class AnalyzeResponse(BaseModel):
    """Response model for contract analysis."""
    account_id: str
    risk_score: int = Field(ge=0, le=100)
    risk_drivers: List[RiskDriver]
    expansion_ops: List[Dict[str, str]]
    playbook: List[PlaybookItem]
    comms: Comms
    metrics: Dict[str, int | float]