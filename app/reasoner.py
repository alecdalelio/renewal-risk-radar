"""
AI reasoning module for contract analysis.
"""

from .models import AnalyzeResponse, RiskDriver, PlaybookItem, Comms


def score_account(features: dict, snippets: list[str], account_id: str) -> AnalyzeResponse:
    """Score account renewal risk and generate recommendations.
    
    Args:
        features: Dictionary of computed features
        snippets: List of redacted note snippets
        account_id: Account identifier
        
    Returns:
        Complete analysis response with risk score and recommendations
    """
    # Calculate risk score based on features
    risk_score = _calculate_risk_score(features)
    
    # Generate risk drivers
    risk_drivers = _generate_risk_drivers(features)
    
    # Generate expansion opportunities
    expansion_ops = _generate_expansion_opportunities(features, snippets)
    
    # Generate playbook
    playbook = _generate_playbook(features, risk_score)
    
    # Generate communications
    comms = _generate_comms(account_id, risk_score, snippets)
    
    return AnalyzeResponse(
        account_id=account_id,
        risk_score=risk_score,
        risk_drivers=risk_drivers,
        expansion_ops=expansion_ops,
        playbook=playbook,
        comms=comms,
        metrics=features
    )


def _calculate_risk_score(features: dict) -> int:
    """Calculate overall risk score from features."""
    base_score = 50  # neutral starting point
    
    # DAU trend impact
    dau_trend = features.get("dau_trend_mom", 0)
    if dau_trend < -0.1:  # 10% decline
        base_score += 30
    elif dau_trend < -0.05:  # 5% decline
        base_score += 15
    elif dau_trend > 0.1:  # 10% growth
        base_score -= 15
    
    # License utilization impact
    utilization = features.get("license_utilization", 0)
    if utilization < 0.5:  # Low utilization
        base_score += 20
    elif utilization > 0.9:  # High utilization (expansion opportunity)
        base_score -= 10
    
    # Support ticket impact
    sev1_tickets = features.get("sev1_last_14d", 0)
    base_score += sev1_tickets * 15  # Each sev1 adds risk
    
    return max(0, min(100, base_score))


def _generate_risk_drivers(features: dict) -> list[RiskDriver]:
    """Generate list of risk drivers based on features."""
    drivers = []
    
    dau_trend = features.get("dau_trend_mom", 0)
    if dau_trend < -0.05:
        drivers.append(RiskDriver(
            signal="Declining DAU",
            weight=0.8,
            explanation=f"Daily active users down {abs(dau_trend):.1%} month-over-month"
        ))
    
    utilization = features.get("license_utilization", 0)
    if utilization < 0.6:
        drivers.append(RiskDriver(
            signal="Low License Utilization",
            weight=0.6,
            explanation=f"Only {utilization:.1%} of licensed seats in use"
        ))
    
    sev1_tickets = features.get("sev1_last_14d", 0)
    if sev1_tickets > 0:
        drivers.append(RiskDriver(
            signal="Critical Support Issues",
            weight=0.7,
            explanation=f"{sev1_tickets} severity 1 tickets in last 14 days"
        ))
    
    return drivers


def _generate_expansion_opportunities(features: dict, snippets: list[str]) -> list[dict[str, str]]:
    """Generate expansion opportunities."""
    opportunities = []
    
    utilization = features.get("license_utilization", 0)
    if utilization > 0.85:
        opportunities.append({
            "opportunity": "Seat Expansion",
            "description": f"High utilization ({utilization:.1%}) indicates need for additional seats"
        })
    
    # Check snippets for expansion hints
    snippet_text = " ".join(snippets).lower()
    if "teams" in snippet_text or "team" in snippet_text:
        opportunities.append({
            "opportunity": "Teams Feature",
            "description": "Customer mentions team collaboration needs"
        })
    
    if "api" in snippet_text:
        opportunities.append({
            "opportunity": "API Tier Upgrade",
            "description": "Customer showing increased API usage patterns"
        })
    
    return opportunities


def _generate_playbook(features: dict, risk_score: int) -> list[PlaybookItem]:
    """Generate recommended actions based on risk level."""
    playbook = []
    
    if risk_score > 70:
        playbook.extend([
            PlaybookItem(
                owner="CSM",
                action="Schedule immediate health check call",
                eta_days=2
            ),
            PlaybookItem(
                owner="Support",
                action="Review and prioritize outstanding tickets",
                eta_days=1
            )
        ])
    elif risk_score > 50:
        playbook.append(PlaybookItem(
            owner="CSM",
            action="Conduct quarterly business review",
            eta_days=7
        ))
    
    utilization = features.get("license_utilization", 0)
    if utilization > 0.85:
        playbook.append(PlaybookItem(
            owner="Sales",
            action="Present seat expansion proposal",
            eta_days=14
        ))
    
    return playbook


def _generate_comms(account_id: str, risk_score: int, snippets: list[str]) -> Comms:
    """Generate communication templates."""
    if risk_score > 70:
        slack_msg = f"🚨 HIGH RISK: {account_id} (score: {risk_score}). Immediate attention needed."
        email_subject = "Partnership Health Check"
    elif risk_score > 50:
        slack_msg = f"⚠️ MEDIUM RISK: {account_id} (score: {risk_score}). Schedule check-in."
        email_subject = "Quarterly Partnership Review"
    else:
        slack_msg = f"✅ LOW RISK: {account_id} (score: {risk_score}). Continue monitoring."
        email_subject = "Partnership Update"
    
    email_body = f"""Hi [CHAMPION_NAME],

Hope you're doing well! I wanted to reach out regarding our partnership and see how things are going with [PRODUCT_NAME].

{f"I noticed some areas where we might be able to help: {', '.join(snippets[:1])}" if snippets else ""}

Would you have time for a brief call this week to discuss how we can better support your team's goals?

Best regards,
[CSM_NAME]"""
    
    return Comms(
        internal_slack=slack_msg,
        client_email=f"Subject: {email_subject}\n\n{email_body}"
    )


def analyze_contract_risk(features: dict) -> dict:
    """Analyze contract renewal risk using AI reasoning.
    
    Args:
        features: Dictionary of extracted features
        
    Returns:
        Dictionary containing risk analysis results
    """
    # TODO: Implement AI-powered risk analysis
    return {}


def generate_insights(analysis: dict) -> list:
    """Generate actionable insights from risk analysis.
    
    Args:
        analysis: Risk analysis results
        
    Returns:
        List of actionable insights
    """
    # TODO: Implement insight generation
    return []
