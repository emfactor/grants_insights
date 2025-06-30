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
            "Recipient Name", "Amount Awarded (GBP)",
            "Grant Title", "Grant Description", "Award Date", "Funding Organisation"
        ]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Missing columns: {missing}")
            return pd.DataFrame()
        df["Award Date"] = pd.to_datetime(df["Award Date"], errors='coerce')
        df["Year"] = df["Award Date"].dt.year
        df["Text"] = df["Grant Title"].fillna('') + ". " + df["Grant Description"].fillna('')
        return df.dropna(subset=["Award Date"])
    except FileNotFoundError:
        st.error("❌ Error: `grants.csv` file not found in the repository.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

with st.sidebar:
    st.header("🔍 Filter Grants")
    query = st.text_input("Search keyword (e.g. climate, children, education)")
    year_range = st.slider(
        "Select Year Range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(2015, 2024)
    )

filtered_df = df[df["Year"].between(year_range[0], year_range[1])]

# Apply fuzzy matching if query exists
if query:
    matches = process.extract(
        query,
        filtered_df["Text"],
        scorer=fuzz.WRatio,
        limit=100
    )
    matched_indices = [match[2] for match in matches if match[1] > 60]
    filtered_df = filtered_df.iloc[matched_indices]

st.write(f"### 🎁 Showing {len(filtered_df)} matching grants")
st.dataframe(
    filtered_df[[
        "Recipient Name", "Amount Awarded (GBP)", "Grant Title",
        "Grant Description", "Award Date", "Funding Organisation"
    ]],
    use_container_width=True
)
