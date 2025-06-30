import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

st.set_page_config(page_title="UK Grant Finder", layout="wide")
st.title("🎯 UK Grant Finder Dashboard")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("grants.csv")
        required_columns = [
            "Recipient Name", "Amount Awarded (GBP)", "Grant Title",
            "Grant Description", "Award Date", "Funding Organisation"
        ]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"❌ Missing columns: {missing}")
            return pd.DataFrame()

        # Clean and parse dates
        df["Date"] = pd.to_datetime(df["Award Date"], errors="coerce")
        df = df.dropna(subset=["Date"]).copy()  # Drop rows without valid dates

        df["Year"] = df["Date"].dt.year.astype(int)
        df["Month"] = df["Date"].dt.strftime("%b")
        return df

    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Grants")

    query = st.text_input("Search keyword (e.g. children, environment)")

    # Year dropdown with All option
    all_years = sorted(df["Year"].dropna().unique(), reverse=True)
    year_options = ["All Years"] + [str(y) for y in all_years[:2]]
    selected_year = st.selectbox("Select Year", year_options)

    # Month multiselect
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    selected_months = st.multiselect("Select Months", month_names, default=month_names)

# --- Apply Filters ---
filtered_df = df.copy()

if selected_year != "All Years":
    try:
        filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]
    except ValueError:
        st.warning("Invalid year selected.")
        st.stop()

filtered_df = filtered_df[filtered_df["Month"].isin(selected_months)]

# --- Smart Fuzzy Search ---
if query:
    combined_text = (filtered_df["Grant Title"].fillna('') + " " +
                     filtered_df["Grant Description"].fillna('')).tolist()
    matches = process.extract(
        query, combined_text, scorer=fuzz.WRatio, limit=100
    )
    matched_indices = [match[2] for match in matches if match[1] > 60]
    if matched_indices:
        filtered_df = filtered_df.iloc[matched_indices]
    else:
        filtered_df = pd.DataFrame()

# --- Show Results ---
st.write(f"### 🎁 Showing {len(filtered_df)} matching grants")

if not filtered_df.empty:
    st.dataframe(
        filtered_df[[
            "Recipient Name",
            "Amount Awarded (GBP)",
            "Grant Title",
            "Grant Description",
            "Award Date",
            "Funding Organisation"
        ]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("No matching grants found. Try changing filters or search term.")
