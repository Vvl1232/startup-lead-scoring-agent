# 🧪 Biotech Decision-Maker Lead Pipeline

## 1️⃣ Project Overview
AI-powered lead identification, enrichment, and scoring pipeline for biotech BD teams. This tool processes potential leads, enriches them with relevant business signals, and ranks them based on strategic importance.

## 2️⃣ Scoring Logic

### Role Fit: +30 points
- Toxicology / Safety roles
- Executive positions (C-level, VP, Director)
- R&D leadership

### Scientific Impact: +40 points
- Number of publications
- Citations and h-index
- Patents filed/granted

### Business Signals: +20 points
- Company funding stage
- Recent funding rounds
- Strategic partnerships

### Location: +10 points
- Biotech hubs (Boston, Bay Area, etc.)
- Proximity to research institutions
- Market presence in key regions

## 3️⃣ How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the pipeline:
   ```bash
   python src/main.py
   ```

3. View the Streamlit dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```

## 4️⃣ Live Outputs

- **Google Sheet**: [View Live Sheet](https://docs.google.com/spreadsheets/d/19Kpm88NnI0EZ4G_nNHJzXgBuGdNoPTSA4IQ1yQ8D_zw/edit)
- **Streamlit Dashboard**: Run locally with `streamlit run streamlit_app.py`

## 5️⃣ Assumptions

- **Mock Data**: Uses sample data in `data/ranked_leads.json`
- **No Web Scraping**: Static data only, no live LinkedIn/web scraping
- **Reproducible Design**: Deterministic pipeline with pinned dependencies
- **Service Account**: Uses Google Sheets API with service account authentication

## Project Structure

```
biotech-lead-pipeline/
│
├── README.md           # This file
├── requirements.txt    # Python dependencies
│
├── data/               # Data files
│   ├── raw_leads.json
│   └── ranked_leads.json
│
├── src/                # Pipeline source code
│   ├── identify.py     # Lead identification
│   ├── enrich.py       # Data enrichment
│   ├── score.py        # Lead scoring logic
│   ├── export_sheet.py # Google Sheets export
│   └── main.py         # Main pipeline
│
└── streamlit_app.py    # Interactive dashboard
```