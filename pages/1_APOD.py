import streamlit as st
import requests
from utils import api_helpers

def main():

    if "data" not in st.session_state:

        url = f"https://api.nasa.gov/planetary/apod?api_key={api_helpers.get_api()}"
        
        response = requests.get(url)
        
        data = response.json()
        st.session_state.data = data
        st.write(response)
        # dict_keys(['copyright', 'date', 'explanation', 'hdurl', 'media_type', 'service_version', 'title', 'url'])
        st.image(data['hdurl'])
    else:

        st.write(st.session_state.data["title"])

    st.button("Rerun")





if __name__ == '__main__':

    main()