import streamlit as st
import pandas as pd
from datetime import datetime
from rapidfuzz import process, fuzz

st.set_page_config(page_title="UK Grant Finder Dashboard", layout="wide")
st.title("🎯 UK Grant Finder Dashboard")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("grants.csv")
        required_columns = [
            "Recipient Name", "Amount Awarded (GBP)",
            "Grant Title", "Grant Description", "Award Date",
            "Funding Organisation"
        ]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Missing columns in CSV: {missing}")
            return pd.DataFrame()

        df["Date"] = pd.to_datetime(df["Award Date"], errors='coerce')
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.strftime("%b")
        df.dropna(subset=["Date"], inplace=True)

        return df
    except FileNotFoundError:
        st.error("❌ Error: 'grants.csv' not found in the repo.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Grants")

    query = st.text_input("Search keyword (e.g. children, education)")

    all_years = sorted(df["Year"].dropna().unique(), reverse=True)
    year_options = ["All Years"] + [str(y) for y in all_years[:2]]
    selected_year = st.selectbox("Select Year", year_options)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    selected_months = st.multiselect("Select Month(s)", month_names, default=month_names)

# Filtering Logic
filtered_df = df.copy()

if selected_year != "All Years":
    filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]

filtered_df = filtered_df[filtered_df["Month"].isin(selected_months)]

# Smart Fuzzy Search
if query:
    combined_text = filtered_df["Grant Title"].fillna("") + " " + filtered_df["Grant Description"].fillna("")
    matches = process.extract(
        query,
        combined_text.tolist(),
        scorer=fuzz.token_set_ratio,
        limit=100
    )
    matched_indices = [i for i, score in [(i, s) for (_, s, i) in matches] if score > 60]

    if matched_indices:
        filtered_df = filtered_df.iloc[matched_indices]
    else:
        st.warning("No close matches found. Try different keywords.")

# Final Output
st.markdown(f"### 🎁 {len(filtered_df)} grant(s) found")
st.dataframe(
    filtered_df[[
        "Recipient Name", "Amount Awarded (GBP)",
        "Grant Title", "Grant Description",
        "Award Date", "Funding Organisation"
    ]],
    use_container_width=True
)
