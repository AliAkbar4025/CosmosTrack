import os
from dotenv import load_dotenv
import streamlit as st
import json

def get_api():
    
    load_dotenv()
    try:
        return st.secrets["NASA_API_KEY"]
    except:
        return os.getenv("NASA_API_KEY")

def get_groq_api():

    load_dotenv()
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

FAVORITES_FILE = "database/favorites.json"

def load_favorites():

    os.makedirs("database", exist_ok=True)
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_favorites(favorites):

    os.makedirs("database", exist_ok=True)
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)