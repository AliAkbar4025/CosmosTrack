import streamlit as st

st.set_page_config(
    page_title="CosmosTrack",
    page_icon="🚀",
    layout="wide"
)

# Navigation
pages = {
    "🌌 CosmosTrack": [
        st.Page("pages/1_APOD.py", title="Picture of the Day", icon="📸"),
        st.Page("pages/2_Asteroids.py", title="Asteroid Tracker", icon="☄️"),
    ]
}

pg = st.navigation(pages)
pg.run()