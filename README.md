# 🎯 UK Grant Finder Dashboard (with Smart Fuzzy Search)

A simple, smart, and fast web app to help users explore UK grant data without requiring any technical skills.

This app uses **fuzzy string matching** (via `rapidfuzz`) to provide intelligent search results, even if users don’t know the exact keywords. Built with `Streamlit` and hosted on the cloud, it's suitable for non-profits, data enthusiasts, and grant seekers.

---

## 🚀 Features

- 🔍 **Fuzzy keyword search** across grant titles and descriptions
- 🕵️‍♀️ Intelligent results even with partial or imperfect terms (e.g. _“children”_ matches _“children’s hospice”_)
- 📅 Filter by year range
- 📊 Instant search results with interactive table
- 🧠 No technical skills required to use or deploy

---

## 🖥 Live App

> [Click here to use the live app](https://[your-streamlit-cloud-url])  
> *(Replace this with your actual link after deploying on Streamlit Cloud)*

---

## 📁 Files in This Repo

- `app.py` — Main Streamlit dashboard
- `grants.csv` — Public UK grant data (20,000+ records)
- `requirements.txt` — Python dependencies
- `README.md` — This file

---

## 🧑‍💻 For Developers

### 🧱 Requirements

- Python 3.8+
- pip

### 📦 Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/grants-finder.git
cd grants-finder

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate       # On Windows
# source venv/bin/activate  # On macOS/Linux

# 3. Install required libraries
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
