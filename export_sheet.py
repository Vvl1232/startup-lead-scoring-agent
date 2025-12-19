import json
import gspread
from google.oauth2.service_account import Credentials
import os

# ---------- CONFIG ----------
SERVICE_ACCOUNT_FILE = "service_account.json"
SHEET_NAME = "Biotech Leads – Demo"
INPUT_FILE = "ranked_leads.json"

# ---------- AUTH ----------
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]
_DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"

def _pick_first_existing_file(candidates):
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None

def _extract_spreadsheet_id(value):
    if not value:
        return None
    value = value.strip()
    if "/spreadsheets/d/" in value:
        try:
            return value.split("/spreadsheets/d/", 1)[1].split("/", 1)[0]
        except Exception:
            return None
    return value

def get_credentials():
    service_account_file = _pick_first_existing_file(
        [
            SERVICE_ACCOUNT_FILE,
            "service_account.json.json",
        ]
    )
    if not service_account_file:
        raise FileNotFoundError(
            "Service account file not found. Expected service_account.json (or service_account.json.json) in project root."
        )
    return Credentials.from_service_account_file(service_account_file, scopes=scopes)

def get_client():
    return gspread.authorize(get_credentials())

def get_sheet(client):
    # Hardcoded spreadsheet ID for convenience
    spreadsheet_id = "19Kpm88NnI0EZ4G_nNHJzXgBuGdNoPTSA4IQ1yQ8D_zw"
    # Fallback to environment variables if needed
    if not spreadsheet_id:
        spreadsheet_id = _extract_spreadsheet_id(
            os.getenv("SPREADSHEET_ID")
            or os.getenv("SHEET_ID")
            or os.getenv("SPREADSHEET_URL")
            or os.getenv("SHEET_URL")
        )
    if spreadsheet_id:
        return client.open_by_key(spreadsheet_id).sheet1
    raise RuntimeError(
        "Missing SPREADSHEET_ID/SHEET_ID (or SPREADSHEET_URL). "
        "Provide the spreadsheet id from a URL like https://docs.google.com/spreadsheets/d/<ID>/edit . "
        "Example (PowerShell): $env:SPREADSHEET_ID=\"<ID>\""
    )

def load_data(input_file):
    resolved_input_file = _pick_first_existing_file(
        [
            input_file,
            INPUT_FILE,
            os.path.join("data", "ranked_leads.json"),
            "ranked_leads.json",
        ]
    )
    if not resolved_input_file:
        raise FileNotFoundError(
            "Input file not found. Expected ranked_leads.json (or data/ranked_leads.json)."
        )
    with open(resolved_input_file, "r", encoding="utf-8") as f:
        return json.load(f)

def push_to_sheet(leads=None):
    client = get_client()
    sheet = get_sheet(client)
    if leads is None:
        leads = load_data(INPUT_FILE)

    # ---------- CLEAR OLD DATA ----------
    sheet.clear()

    # ---------- HEADER ----------
    headers = [
        "Rank",
        "Score",
        "Name",
        "Title",
        "Company",
        "Location",
        "LinkedIn",
        "Score Breakdown"
    ]

    sheet.append_row(headers)

    # ---------- INSERT ROWS ----------
    for idx, lead in enumerate(leads, start=1):
        rank = lead.get("rank", idx)
        score = lead.get("score", "")
        score_breakdown = lead.get("score_breakdown")
        if score_breakdown is None:
            score_breakdown = lead.get("reason", "")
        if not isinstance(score_breakdown, str):
            score_breakdown = json.dumps(score_breakdown)

        sheet.append_row([
            rank,
            score,
            lead.get("name", ""),
            lead.get("title", ""),
            lead.get("company", ""),
            lead.get("location", ""),
            lead.get("linkedin", ""),
            score_breakdown,
        ])

    print(" Google Sheet updated successfully!")

if __name__ == "__main__":
    push_to_sheet()