# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Grant Insights Finder", layout="wide")
st.title("💸 UK Grant Insights Finder")

# Upload CSV
st.sidebar.header("Upload Your Grants CSV")
uploaded_file = st.sidebar.file_uploader("Upload grants.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Basic check
    required_cols = ['Grant Title', 'Description of Grant']
    if not all(col in df.columns for col in required_cols):
        st.error("CSV must contain at least 'Grant Title' and 'Description of Grant' columns.")
    else:
        # Sidebar filters
        if 'Funder' in df.columns:
            funder_filter = st.sidebar.multiselect("Select Funders:", df['Funder'].dropna().unique())
        else:
            funder_filter = []

        if 'Award Year' in df.columns:
            year_filter = st.sidebar.multiselect("Select Years:", sorted(df['Award Year'].dropna().unique()))
        else:
            year_filter = []

        # Apply filters
        filtered_df = df.copy()
        if funder_filter:
            filtered_df = filtered_df[filtered_df['Funder'].isin(funder_filter)]
        if year_filter:
            filtered_df = filtered_df[filtered_df['Award Year'].isin(year_filter)]

        # Search
        st.subheader("🔍 Search for Grants")
        query = st.text_input("Enter keywords (e.g. youth, environment, training):")

        if query:
            results = filtered_df[
                filtered_df['Grant Title'].str.contains(query, case=False, na=False) |
                filtered_df['Description of Grant'].str.contains(query, case=False, na=False)
            ]
            st.markdown(f"### Top {min(len(results), 10)} Results")
            st.dataframe(results[['Grant Title', 'Funder', 'Amount Awarded', 'Award Year', 'Description of Grant']].head(10))
        else:
            st.info("Enter a keyword above to search grants.")

        # Charts
        if 'Award Year' in filtered_df.columns and 'Amount Awarded' in filtered_df.columns:
            st.subheader("📊 Grant Amount by Year")
            year_chart = filtered_df.groupby('Award Year')['Amount Awarded'].sum().reset_index()
            fig = px.bar(year_chart, x='Award Year', y='Amount Awarded', title='Total Grant Amount by Year')
            st.plotly_chart(fig, use_container_width=True)

        if 'Funder' in filtered_df.columns and 'Amount Awarded' in filtered_df.columns:
            st.subheader("🏢 Top Funders")
            top_funders = filtered_df.groupby('Funder')['Amount Awarded'].sum().nlargest(10).reset_index()
            fig2 = px.pie(top_funders, values='Amount Awarded', names='Funder', title='Top 10 Funders by Amount')
            st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Upload your grants CSV using the sidebar.")
