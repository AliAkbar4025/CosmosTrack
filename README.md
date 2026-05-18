# 🚀 CosmosTrack

An interactive NASA data explorer built with Streamlit.

---

## 📸 Page 1 — APOD Viewer
- View today's Astronomy Picture of the Day
- Look up APOD for any date
- Save favourites
- Favourites are stored locally and shared across sessions on the cloud version.

## ☄️ Page 2 — Asteroid Tracker
- Live near-Earth asteroid data from NASA NeoWs API
- 2D orbital proximity plot
- Stats: total count, hazardous count, closest approach, largest object
- Full data table with CSV download
- AI-generated analyst report + follow-up chat (Groq LLaMA 3.3 70B)

---

## ⚙️ Setup

```bash
git clone https://github.com/yourusername/CosmosTrack.git
cd cosmostrack
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml`:
```toml
NASA_API_KEY = "your_nasa_api_key"
GROQ_API_KEY = "your_groq_api_key"
```

Get your keys:
- NASA → https://api.nasa.gov
- Groq → https://console.groq.com

---

## 📦 Requirements

```
streamlit
requests
plotly
pandas
pillow
python-dotenv
```

---

## 🙋 Author

Built by Ali — ML Developer & Streamlit enthusiast.