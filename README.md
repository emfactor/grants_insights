# UK Grant Insights Finder

A simple Streamlit dashboard to explore and search UK grant data based on keywords, funders, and years. Useful for charities, researchers, and funding analysts.

## 🔧 How to Use

### 📦 Upload CSV

1. Click on the sidebar and upload a CSV file.
2. Ensure your CSV has at least these columns:
   - `Grant Title`
   - `Description of Grant`
   - Optional: `Funder`, `Award Year`, `Amount Awarded`

### 🔍 Search Features

- Type in a keyword to find matching grants.
- Filter by funder or award year.
- View top 10 search results and interactive charts.

---

## 🛰️ Deploy to Streamlit Cloud

1. Create a free account on [Streamlit Cloud](https://streamlit.io/cloud)
2. Upload this project (with `app.py`, `requirements.txt`, and optionally a sample CSV) to GitHub.
3. On Streamlit Cloud, click **New App** → Select your GitHub repo → Deploy.

---

## 📂 Example File Format

| Grant Title         | Description of Grant              | Funder       | Award Year | Amount Awarded |
|---------------------|-----------------------------------|--------------|-------------|-----------------|
| Youth Empowerment   | Supporting youth digital skills   | ABC Foundation | 2023       | 10000          |

---

## 🧑 For Non-Technical Users

You only need to:
- Upload your CSV file via the sidebar.
- Use filters and keyword search. No coding required!

---

## 🧪 Requirements

- `streamlit`
- `pandas`
- `plotly`
