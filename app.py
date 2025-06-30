import streamlit as st
import pandas as pd
from rapidfuzz import process

st.set_page_config(page_title="UK Grants Finder", layout="wide")
st.title("🧠 UK Grant Finder with Fuzzy Search")

@st.cache_data
def load_data():
    df = pd.read_csv("grants.csv")
    df["Date"] = pd.to_datetime(df["Award Date"], errors="coerce")
    df["Year"] = df["Date"].dt.year
    df["Text"] = df["Grant Title"].fillna("") + ". " + df["Grant Description"].fillna("")
    return df

df = load_data()

with st.sidebar:
    st.header("🔍 Search")
    query = st.text_input("Search keyword", value="children")
    year_range = st.slider("Filter by year", int(df["Year"].min()), int(df["Year"].max()), (2015, 2024))

# Filter by year
df = df[df["Year"].between(year_range[0], year_range[1])]

# Fuzzy match top 50 relevant rows
if query:
    matches = process.extract(
        query,
        df["Text"],
        limit=50,
        scorer=process.fuzz.WRatio  # or fuzz.token_set_ratio
    )
    matched_indices = [match[2] for match in matches]
    df = df.iloc[matched_indices]

st.markdown(f"### 🎯 Showing {len(df)} results for '**{query}**'")
st.dataframe(
    df[[
        "Recipient Name", "Amount Awarded (GBP)", "Grant Title",
        "Grant Description", "Award Date", "Funding Organisation"
    ]],
    use_container_width=True
)
