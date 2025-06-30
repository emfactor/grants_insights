# 💡 UK Charity Grant Finder & Smart Matcher

An AI-powered Streamlit app to help UK-based charities discover relevant funding opportunities — instantly.

Built in under a day to demonstrate innovation, real-world impact, and practical deployment, this app uses open data + NLP to enable smaller organisations to access crucial funding.

---

## 🚀 Features

✅ Explore 90,000+ UK grant records  
✅ Smart grant matching using `sentence-transformers`  
✅ Filter by region, funder, and timeline  
✅ Visualise trends by amount, region, or funder  
✅ Deployable instantly via [Streamlit Cloud](https://streamlit.io/cloud) — no setup required  

---

## 🧠 How Smart Matching Works

Describe your project (e.g. _“We support homeless youth with mental health challenges in Manchester”_) and the app uses NLP to:

- Convert your text to a semantic vector
- Match it against thousands of real UK grant descriptions
- Return the **5 closest funding opportunities** — ranked by meaning, not keywords

---

## 📁 Project Structure
📦 grant-finder-app/
├── app.py # Streamlit app
├── requirements.txt # Dependencies
├── cleaned_grants_dataset.csv # UK grant data (pre-cleaned)
└── README.md
