import streamlit as st
import requests
from utils import api_helpers
import datetime
import plotly.graph_objects as go
import math
import random
import pandas as pd
from groq import Groq


def main():

    st.title("Asteroid Tracker")
    st.divider()

    if "Data_NeoWs" not in st.session_state:

        API_KEY = api_helpers.get_api()

        today = datetime.date.today()
        week_later = today + datetime.timedelta(days=7)

        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={week_later}&api_key={API_KEY}"

        st.session_state.dateRange = f"{today} - {week_later}"

        response = requests.get(url)

        if response.status_code == 200:
            st.session_state.Data_NeoWs = response.json()
        else:
            st.error("Failed to fetch NASA data")
            st.stop()

    NeoWsData = st.session_state.Data_NeoWs
    dateRange = st.session_state.get("dateRange", "N/A")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers+text",
            marker=dict(size=30, color="blue"),
            text=["Earth"],
            name="Earth"
        )
    )

    hazardous_ast = 0
    lowest_magnitude = float("inf")

    hazardous_asteroids = []
    miss_distance = []
    magnitude = []
    name = []
    approach_date = []
    neo_id = []
    url_list = []
    velocity_list = []

    for key, asteroid_list in NeoWsData["near_earth_objects"].items():

        for asteroid in asteroid_list:

            if not asteroid["close_approach_data"]:
                continue

            approach = asteroid["close_approach_data"][0]

            distance = float(approach["miss_distance"]["kilometers"])
            distance_scaled = distance / 1000000

            hazardous = asteroid["is_potentially_hazardous_asteroid"]

            if hazardous:
                hazardous_ast += 1

            asteroid_size = 30 - asteroid["absolute_magnitude_h"]
            asteroid_size = max(5, min(asteroid_size, 25))

            if asteroid["absolute_magnitude_h"] < lowest_magnitude:
                lowest_magnitude = asteroid["absolute_magnitude_h"]

            date = approach["close_approach_date"]

            random.seed(date + asteroid["name"])

            angle = random.uniform(0, 360)
            angle_rad = math.radians(angle)

            x = distance_scaled * math.cos(angle_rad)
            y = distance_scaled * math.sin(angle_rad)

            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers",
                    marker=dict(
                        size=asteroid_size,
                        color="red" if hazardous else "green"
                    ),
                    text=f"Name: {asteroid['name']}",
                    name=asteroid["name"]
                )
            )

            hazardous_asteroids.append(hazardous)
            miss_distance.append(distance)
            magnitude.append(asteroid["absolute_magnitude_h"])
            name.append(asteroid["name"])
            approach_date.append(date)
            neo_id.append(asteroid["neo_reference_id"])
            url_list.append(asteroid["nasa_jpl_url"])

            velocity_kmh = float(asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
            velocity_list.append(velocity_kmh)

    df = pd.DataFrame({
        "neo_id": neo_id,
        "name": name,
        "approach_date": approach_date,
        "url": url_list,
        "magnitude": magnitude,
        "miss_distance_km": miss_distance,
        "is_hazardous": hazardous_asteroids,
        "velocity_kmh": velocity_list
    })

    fig.update_layout(
        xaxis_title="Distance (million km)",
        yaxis_title="Distance (million km)",
        showlegend=False
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total asteroids tracked this week",
            value=int(NeoWsData["element_count"])
        )

    with col2:
        st.metric(
            "Hazardous asteroids",
            value=hazardous_ast
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Largest Asteroid (Lowest Magnitude)",
            value=round(lowest_magnitude, 2)
        )

    with col2:
        closest_distance = min(miss_distance) if miss_distance else 0
        st.metric(
            "Closest Approach (km)",
            value=f"{closest_distance:,.0f}"
        )

    st.divider()

    st.markdown("# Asteroids Plot:")
    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.markdown("# Data:")
    st.dataframe(df, width="stretch")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name="NASA_Asteroids.csv",
        mime="text/csv"
    )

    st.divider()

    GROQ_API_KEY = api_helpers.get_groq_api()

    metaData = {
        "Total Asteroids": int(NeoWsData['element_count']),
        "Date Range": dateRange
    }

    astData = {
        "name": name,
        "approach_date": approach_date,
        "hazardous": hazardous_asteroids,
        "magnitude": magnitude,
        "miss_distance_km": miss_distance,
        "velocity_kmh": velocity_list
    }

    system_prompt = f"""You are a senior analyst at NASA's Planetary Defense Coordination Office.
You have already analyzed this asteroid data:
Asteroid Data: {astData}
Meta Data: {metaData}
Answer any follow-up questions confidently. Never mention JSON or that you are an AI."""

    report_prompt = f"""You are a senior analyst at NASA's Planetary Defense Coordination Office.

You have been handed the following asteroid close-approach dataset for analysis.
The data is pre-filtered and contains only essential fields.

Asteroid Data:
{astData}

Meta Data:
{metaData}

Write a professional but engaging NASA-style briefing report using EXACTLY this format:

## 🌍 ASTEROID BRIEFING REPORT

### 1. OVERVIEW
[Total asteroids tracked, date range, how many are potentially hazardous]

### 2. CLOSEST APPROACH
[Asteroid name, miss distance in km, compare to Earth-Moon distance (384,400 km)]

### 3. FASTEST OBJECT
[Name, speed in km/h, compare to something relatable like a bullet or jet]

### 4. LARGEST OBJECT
[Name, magnitude, compare to something familiar like a stadium or city]

### 5. ⚠️ HAZARD SUMMARY
[List each potentially hazardous asteroid on its own line with a bullet point]
[Explain in plain English what hazardous means and give honest risk assessment]

### 6. 💡 ANALYST'S NOTE
[One surprising or interesting insight from the data]

---
*Prepared by NASA Planetary Defense Coordination Office*

Rules:
- Never mention JSON, data formats, or that you are an AI
- Speak as if you personally tracked and analyzed these asteroids
- Follow the format above exactly — do not add or remove sections
- Keep total response under 450 words
- Use bullet points inside sections where listing multiple items
- Every section must have actual content — never say data is unavailable"""

    if "Ast_Report" not in st.session_state:

        with st.spinner("Generating..."):

            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": report_prompt}],
                max_tokens=600
            )

            st.session_state.Ast_Report = response.choices[0].message.content

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("## 🤖 AI Analyst Report")

    with st.chat_message("assistant"):
        st.markdown(st.session_state.Ast_Report)

    st.divider()

    st.markdown("## 💬 Ask the Analyst")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask anything about these asteroids...")

    if question:

        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.chat_history.append({"role": "user", "content": question})

        messages = [{"role": "system", "content": system_prompt}]
        messages += st.session_state.chat_history[-10:]

        with st.spinner("Generating"):

            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
            )
            answer = response.choices[0].message.content

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            
            st.markdown(answer)


if __name__ == "__main__":

    main()