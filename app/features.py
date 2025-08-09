"""
Feature extraction module for contract analysis.
"""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import List, Dict, Any


def _avg(xs: list[float]) -> float:
    """Calculate average of a list of floats."""
    return sum(xs) / len(xs) if xs else 0.0


def compute_features(usage_rows: List[Dict[str, Any]], ticket_rows: List[Dict[str, Any]], notes_text: str | None) -> dict:
    """Extract features from usage data, tickets, and notes.
    
    Args:
        usage_rows: List of usage data dictionaries
        ticket_rows: List of support ticket dictionaries  
        notes_text: Customer notes text
        
    Returns:
        Dictionary of computed features
    """
    def parse_date(s: str) -> datetime:
        """Parse date string with multiple format fallbacks."""
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(str(s), fmt)
            except ValueError:
                continue
        # fallback: today to avoid crashing on bad data
        return datetime.utcnow()

    # Process usage data
    usage = sorted(usage_rows, key=lambda r: parse_date(r.get("date", ""))) if usage_rows else []
    dau = [float(r.get("dau", 0)) for r in usage]
    
    if len(dau) >= 14:
        last7 = _avg(dau[-7:])
        prev7 = _avg(dau[-14:-7])
        dau_trend_mom = 0.0 if prev7 == 0 else (last7 - prev7) / prev7
    else:
        dau_trend_mom = 0.0

    # Calculate license utilization
    if usage:
        last = usage[-1]
        used = float(last.get("used_seats", 0))
        licensed = float(last.get("licensed_seats", 0))
        license_utilization = (used / licensed) if licensed > 0 else 0.0
    else:
        license_utilization = 0.0

    # Count severity 1 tickets in last 14 days
    cutoff = datetime.utcnow() - timedelta(days=14)
    sev1_last_14d = 0
    for t in (ticket_rows or []):
        sev = int(t.get("severity", 0))
        created_at = parse_date(t.get("created_at", "1970-01-01"))
        if sev == 1 and created_at >= cutoff:
            sev1_last_14d += 1

    return {
        "dau_trend_mom": round(dau_trend_mom, 4),
        "license_utilization": round(license_utilization, 4),
        "sev1_last_14d": sev1_last_14d,
    }


def extract_features(contract_text: str) -> dict:
    """Extract features from contract text.
    
    Args:
        contract_text: The contract text to analyze
        
    Returns:
        Dictionary of extracted features
    """
    # TODO: Implement feature extraction logic
    return {}


def calculate_risk_indicators(features: dict) -> dict:
    """Calculate risk indicators from extracted features.
    
    Args:
        features: Dictionary of extracted features
        
    Returns:
        Dictionary of risk indicators
    """
    # TODO: Implement risk indicator calculation
    return {}