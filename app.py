import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="UK Charity Grant Finder", layout="wide")

# --- LOAD DATA & EMBEDDINGS ---
@st.cache_data
def load_data():
    return pd.read_csv("grants.csv")

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_embeddings():
    with open("grant_embeddings.pkl", "rb") as f:
        return pickle.load(f)

df = load_data()
model = load_model()
grant_embeddings = load_embeddings()

# --- UI ---
st.title("💡 UK Charity Grant Finder & Matcher")
st.markdown("Find funding that matches your mission. Powered by AI.")

# --- SMART MATCHING ---
st.header("🔎 Find Relevant Grants")

user_input = st.text_input("Describe your project in 1–2 sentences")

if user_input:
    with st.spinner("Finding top grants..."):
        input_embedding = model.encode(user_input).reshape(1, -1)
        similarities = cosine_similarity(input_embedding, grant_embeddings)[0]
        df["Score"] = similarities
        top_matches = df.sort_values("Score", ascending=False).head(5)

    st.success("Top 5 matched grants")
    st.dataframe(top_matches[["Grant Title", "Grant Description", "Amount Awarded (GBP)", "Region", "Funding Organisation"]])

# --- SIDEBAR FILTERS ---
st.sidebar.header("📍 Filters")
regions = st.sidebar.multiselect("Filter by region", df["Region"].dropna().unique())
funders = st.sidebar.multiselect("Filter by funder", df["Funding Organisation"].dropna().unique())

filtered_df = df.copy()
if regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(regions)]
if funders:
    filtered_df = filtered_df[filtered_df["Funding Organisation"].isin(funders)]

# --- STATS ---
st.subheader("📊 Grant Insights")
col1, col2 = st.columns(2)
col1.metric("Total Grants", f"{filtered_df.shape[0]:,}")
col2.metric("Total Awarded", f"£{int(filtered_df['Amount Awarded (GBP)'].sum()):,}")

# --- CHARTS ---
st.subheader("📍 Funding by Region")
region_chart = filtered_df.groupby("Region")["Amount Awarded (GBP)"].sum().reset_index()
st.plotly_chart(px.bar(region_chart, x="Region", y="Amount Awarded (GBP)", text_auto=True), use_container_width=True)

st.subheader("📅 Timeline")
df["Award Date"] = pd.to_datetime(df["Award Date"], errors="coerce")
filtered_df["Month"] = df["Award Date"].dt.to_period("M").astype(str)
timeline = filtered_df.groupby("Month")["Amount Awarded (GBP)"].sum().reset_index()
st.plotly_chart(px.line(timeline, x="Month", y="Amount Awarded (GBP)", markers=True), use_container_width=True)

# --- FULL TABLE ---
st.subheader("📋 All Matching Grants")
st.dataframe(filtered_df, use_container_width=True)
