def score_lead(lead):
    score = 0
    reasons = []

    if "Toxicology" in lead["title"] or "Safety" in lead["title"]:
        score += 30
        reasons.append("Role Fit +30")

    if lead["recent_publication"]:
        score += 40
        reasons.append("Scientific Intent +40")

    if lead["company_funded"]:
        score += 20
        reasons.append("Funding Signal +20")

    if lead["is_hub"]:
        score += 10
        reasons.append("Hub Location +10")

    return score, " | ".join(reasons)