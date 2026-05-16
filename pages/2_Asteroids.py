import streamlit as st
import requests
from utils import api_helpers
import datetime
import plotly.graph_objects as go
import math
import random

def main():

    if "Data_NeoWs" not in st.session_state:

        API_KEY = api_helpers.get_api()
        today = datetime.date.today()
        week_later = today + datetime.timedelta(days=7)

        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={week_later}&api_key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        st.session_state.Data_NeoWs = data

        
    
    NeoWsData = st.session_state.Data_NeoWs
    st.title("Asteroids")
    st.divider()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0], 
        y=[0],
        mode='markers+text',
        marker=dict(size=30, color='blue'),
        text=['Earth'],
        name='Earth'
    ))
    
    for key, data in NeoWsData["near_earth_objects"].items():

        for asteroid in data:

            distance = float(asteroid["close_approach_data"][0]["miss_distance"]["kilometers"])
            distance_scaled = distance / 1000000
            
            hazardous = asteroid["is_potentially_hazardous_asteroid"]
            
            asteroid_size = 30 - asteroid["absolute_magnitude_h"]
            asteroid_size = max(5, min(asteroid_size, 25))
            
            date = asteroid['close_approach_data'][0]['close_approach_date']
            random.seed(date + asteroid['name'])
            angle = random.uniform(0, 360)
            angle_rad = math.radians(angle)
            
            x = distance_scaled * math.cos(angle_rad)
            y = distance_scaled * math.sin(angle_rad)

            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers',
                marker=dict(
                    size=asteroid_size,
                    color='red' if hazardous else 'green'
                ),
                text=asteroid['name'],
                name=asteroid['name']
            ))
    
    fig.update_layout(
        xaxis_title="Distance (million km)",
        yaxis_title="Distance (million km)",
        showlegend=False
    )
    
    st.plotly_chart(fig)


if __name__ == "__main__":

    main()