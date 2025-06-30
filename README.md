# UK Grants Insights Dashboard

🎯 A simple Streamlit web app that helps non-technical users find UK grants by cause, year, and keywords. No setup required.

---

## 📦 What's Included

- `app.py` — the Streamlit app
- `grants.csv` — sample data (~20k UK grant records)
- `requirements.txt` — Streamlit + Pandas

---

## 🚀 How to Run (No Coding Needed)

### Option 1: Run in Streamlit Cloud
1. Create a free account at [streamlit.io](https://streamlit.io)
2. Fork this GitHub repo into your account
3. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub
4. Select this repo and deploy!

☁️ You’ll get a public app link to share.

---

## 🧑‍💼 For Users

When the app opens:
- Use the sidebar to filter by **keyword** (e.g. "climate", "health", "education").
- Use the slider to choose the **year range**.
- Matching grants will appear in a searchable, sortable table.

No upload or setup required!

---

## 🔐 Notes

- All grant data is preloaded in `grants.csv`.
- If the file is missing or broken, the app shows an error message.
