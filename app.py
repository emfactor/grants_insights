import streamlit as st
import pandas as pd
import plotly.express as px
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="UK Charity Grant Finder", layout="wide")

# Load model (can take a few seconds)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_grants_dataset.csv")

df = load_data()

st.title("💡 UK Charity Grant Finder & Insights Dashboard")
st.markdown("Use this dashboard to find relevant UK grants and explore trends in funding data.")

# --- SMART GRANT MATCHING ---
st.header("🔎 Find Matching Grants for Your Project")

user_input = st.text_input("Describe your charity or project in 1–2 sentences")

if user_input:
    with st.spinner("Finding best grant matches..."):
        grant_texts = df["Grant Title"].fillna('') + " " + df["Grant Description"].fillna('')
        grant_embeddings = model.encode(grant_texts.tolist(), convert_to_tensor=True)
        input_embedding = model.encode(user_input, convert_to_tensor=True)

        similarities = cosine_similarity(
            [input_embedding.cpu().numpy()],
            grant_embeddings.cpu().numpy()
        )[0]

        df["Similarity Score"] = similarities
        top_matches = df.sort_values(by="Similarity Score", ascending=False).head(5)

    st.success("Top 5 grant matches for your project:")
    st.dataframe(top_matches[["Grant Title", "Grant Description", "Amount Awarded (GBP)", "Region", "Funding Organisation"]])

# --- FILTERS ---
st.sidebar.header("📍 Filter grants")
regions = st.sidebar.multiselect("Select region(s)", options=df["Region"].dropna().unique(), default=[])
funders = st.sidebar.multiselect("Select funder(s)", options=df["Funding Organisation"].dropna().unique(), default=[])

filtered_df = df.copy()
if regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(regions)]
if funders:
    filtered_df = filtered_df[filtered_df["Funding Organisation"].isin(funders)]

# --- STATS ---
st.subheader("📈 Grant Data Summary")
col1, col2 = st.columns(2)
col1.metric("Total Grants", f"{filtered_df.shape[0]:,}")
col2.metric("Total Awarded", f"£{int(filtered_df['Amount Awarded (GBP)'].sum()):,}")

# --- CHARTS ---
st.subheader("📊 Grant Amounts by Region")
region_chart = filtered_df.groupby("Region")["Amount Awarded (GBP)"].sum().sort_values(ascending=False).reset_index()
fig1 = px.bar(region_chart, x="Region", y="Amount Awarded (GBP)", text_auto=".2s")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📅 Grant Awards Over Time")
df["Award Date"] = pd.to_datetime(df["Award Date"], errors="coerce")
filtered_df["Month"] = df["Award Date"].dt.to_period("M").astype(str)
timeline = filtered_df.groupby("Month")["Amount Awarded (GBP)"].sum().reset_index()
fig2 = px.line(timeline, x="Month", y="Amount Awarded (GBP)", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# --- TABLE ---
st.subheader("📋 All Grants")
st.dataframe(filtered_df, use_container_width=True)
