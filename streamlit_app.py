import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Biotech Lead Ranking",
    layout="wide"
)

st.title("🧬 Biotech Decision-Maker Lead Ranking")
st.caption("Demo pipeline output — ranked leads with filters")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    with open("data/ranked_leads.json", "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

df = load_data()

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Filters")
st.sidebar.caption(f"Total leads loaded: {len(df)}")

min_score_val = int(df["score"].min())
max_score_val = int(df["score"].max())

if min_score_val == max_score_val:
    st.sidebar.info(f"Only one score available: {min_score_val}")
    min_score = min_score_val
else:
    min_score = st.sidebar.slider(
        "Minimum Score",
        min_value=min_score_val,
        max_value=max_score_val,
        value=min_score_val
    )

location_filter = st.sidebar.multiselect(
    "Location",
    options=df["location"].unique(),
    default=df["location"].unique()
)

# ---------- FILTER DATA (DEFINE FIRST!) ----------
filtered_df = df[
    (df["score"] >= min_score) &
    (df["location"].isin(location_filter))
]

# ---------- MAIN TABLE ----------
st.subheader("📊 Ranked Leads")

st.dataframe(
    filtered_df[[
        "rank",
        "score",
        "name",
        "title",
        "company",
        "location",
        "linkedin"
    ]],
    use_container_width=True
)

# ---------- REFRESH ----------
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.experimental_rerun()

# ---------- EXPORT ----------
st.subheader("📤 Export")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="ranked_biotech_leads.csv",
    mime="text/csv"
)
