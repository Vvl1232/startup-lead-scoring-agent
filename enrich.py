def enrich_lead(lead):
    lead["is_hub"] = lead["location"] in [
        "Cambridge, MA", "Boston, MA",
        "San Francisco, CA", "Basel, Switzerland"
    ]

    lead["company_funded"] = lead["company"] != "EarlyBio"
    lead["recent_publication"] = "Toxicology" in lead["title"]

    return lead