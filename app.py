import streamlit as st
import pandas as pd
from datetime import datetime
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
        df["Month"] = df["Award Date"].dt.month
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
    
    # Year Dropdown
    current_year = datetime.now().year
    available_years = [current_year, current_year - 1]
    selected_year = st.selectbox("Select Year", available_years, index=0)

    # Month multiselect buttons
    st.markdown("**Select Month(s)**")
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_numbers = list(range(1, 13))
    month_mapping = dict(zip(month_names, month_numbers))
    
    selected_month_names = st.multiselect(
        "Month(s)",
        options=month_names,
        default=month_names,  # Show all months selected by default
        label_visibility="collapsed"
    )
    selected_months = [month_mapping[m] for m in selected_month_names]

    # Keyword search
    query = st.text_input("Search keyword (e.g. children, hospice, youth)")

# Filter by year and months
filtered_df = df[(df["Year"] == selected_year) & (df["Month"].isin(selected_months))]

# Apply smart search if query exists
# Apply smart search if query exists
if query:
    temp_df = filtered_df.reset_index(drop=True)
    matches = process.extract(
        query,
        temp_df["Text"],
        scorer=fuzz.WRatio,
        limit=100
    )
    matched_indices = [match[2] for match in matches if match[1] > 60]
    filtered_df = temp_df.iloc[matched_indices]


st.write(f"### 🎁 Showing {len(filtered_df)} matching grants")
st.dataframe(
    filtered_df[[
        "Recipient Name", "Amount Awarded (GBP)", "Grant Title",
        "Grant Description", "Award Date", "Funding Organisation"
    ]],
    use_container_width=True
)
