from identify import load_leads
from enrich import enrich_lead
from score import score_lead
from export_sheet import push_to_sheet

leads = load_leads()

final = []
for lead in leads:
    enriched = enrich_lead(lead)
    score, reason = score_lead(enriched)
    enriched["score"] = score
    enriched["reason"] = reason
    final.append(enriched)

final = sorted(final, key=lambda x: x["score"], reverse=True)

push_to_sheet(final)