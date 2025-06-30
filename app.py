import streamlit as st
import pandas as pd

st.set_page_config(page_title="UK Grants Finder", layout="wide")
st.title("🎯 UK Grant Finder Dashboard")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("grants.csv")
        required_columns = ["Recipient Name", "Amount Awarded (GBP)", "Grant Title", "Grant Description", "Award Date", "Funding Organisation"]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Missing columns: {missing}")
            return pd.DataFrame()
        df["Date"] = pd.to_datetime(df["Award Date"], errors='coerce')
        df["Year"] = df["Award Date"].dt.year
        return df
    except FileNotFoundError:
        st.error("❌ Error: `grants.csv` file not found in repo.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

with st.sidebar:
    st.header("🔍 Filter Grants")
    keyword = st.text_input("Search keyword (e.g. climate, education)")
    year_range = st.slider("Year Range", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=(2015, 2024))

filtered_df = df[df["Year"].between(year_range[0], year_range[1])]
if keyword:
    filtered_df = filtered_df[
        df["GTitle"].str.contains(keyword, case=False, na=False) |
        df["Description"].str.contains(keyword, case=False, na=False)
    ]

st.write(f"### 🎁 Showing {len(filtered_df)} matching grants")
st.dataframe(filtered_df[["Recipient Name", "Amount Awarded", "Grant Title", "Description of Grant", "Award Date", "Funding Organisation"]], use_container_width=True)
