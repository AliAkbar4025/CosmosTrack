import streamlit as st
import requests
from utils import api_helpers
import datetime

def main():
    st.title("NASA Astronomy Picture of the Day Gallery")
    st.divider()

    if "data_today" not in st.session_state:
        API_KEY = api_helpers.get_api()
        url_today = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        response_today = requests.get(url_today)
        st.session_state.data_today = response_today.json()
    
    if "favorites" not in st.session_state:
        st.session_state.favorites = api_helpers.load_favorites()

    data = st.session_state.data_today
    
    st.markdown("### Today's APOD:")
    make_PicCard(data.get('hdurl') or data.get('url'), data['title'], APODtype=data['media_type'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Add to favourites", key="fav_today", use_container_width=True):
            if data not in st.session_state.favorites:
                st.session_state.favorites.append(data)
                api_helpers.save_favorites(st.session_state.favorites)
                st.success("Added to favorites!")
            else:
                st.info("Already in favorites")
        
    with col2:
        if st.button("Details", key="details_today", use_container_width=True):
            st.session_state.selected_apod = data
            show_details(st.session_state.selected_apod)
    
    st.divider()

    if "randomAPODs" not in st.session_state:
        API_KEY = api_helpers.get_api()
        random_count = 6
        url_random = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count={random_count}"
        response_random = requests.get(url_random)
        st.session_state.randomAPODs = response_random.json()
    
    randomAPODs = st.session_state.randomAPODs
    mid = len(randomAPODs) // 2
    first_half_APODs = randomAPODs[:mid]
    second_half_APODs = randomAPODs[mid:]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Some APOD's")
    
    with col2:
        if st.button("Refresh", key="refresh_random", use_container_width=True):
            del st.session_state.randomAPODs
            st.rerun()

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        for item in first_half_APODs:
            make_PicCard(item.get('hdurl') or item.get('url'), item['title'], APODtype=item['media_type'])
            
            col_l, col_r = st.columns(2)
            
            with col_l:
                if st.button("Add to favourites", key=f"{item['date']}_fav_left", use_container_width=True):
                    if item not in st.session_state.favorites:
                        st.session_state.favorites.append(item)
                        api_helpers.save_favorites(st.session_state.favorites)
                        st.success("Added!")
                    else:
                        st.info("Already in favorites")
                
            with col_r:
                if st.button("Details", key=f"{item['date']}_details_left", use_container_width=True):
                    st.session_state.selected_apod = item
                    show_details(st.session_state.selected_apod)
    
    with col2:
        for item in second_half_APODs:
            make_PicCard(item.get('hdurl') or item.get('url'), item['title'], APODtype=item['media_type'])
            
            col_l, col_r = st.columns(2)
            
            with col_l:
                if st.button("Add to favourites", key=f"{item['date']}_fav_right", use_container_width=True):
                    if item not in st.session_state.favorites:
                        st.session_state.favorites.append(item)
                        api_helpers.save_favorites(st.session_state.favorites)
                        st.success("Added!")
                    else:
                        st.info("Already in favorites")
                
            with col_r:
                if st.button("Details", key=f"{item['date']}_details_right", use_container_width=True):
                    st.session_state.selected_apod = item
                    show_details(st.session_state.selected_apod)

    st.divider()

    today = datetime.date.today()
    apod_start = datetime.date(1995, 6, 16)

    st.markdown("### Select a Date")

    selected_date = st.date_input(
        "Select APOD Date",
        value=today,
        min_value=apod_start,
        max_value=today,
        format="YYYY-MM-DD"
    )

    if "selectedAPOD" not in st.session_state:
        st.session_state.selectedAPOD = None
        st.session_state.last_date = None

    if st.button("Fetch APOD", key="fetch_selected_date"):
        API_KEY = api_helpers.get_api()
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={selected_date}"
        response = requests.get(url)
        
        if response.status_code == 200:
            st.session_state.selectedAPOD = response.json()
            st.session_state.last_date = selected_date
            st.success("APOD fetched successfully!")
        else:
            st.error("Failed to fetch APOD")
        
        st.divider()

    if st.session_state.selectedAPOD:
        selectedAPOD = st.session_state.selectedAPOD
        
        st.markdown("### Your APOD:")
        make_PicCard(selectedAPOD.get('hdurl') or selectedAPOD.get("url"), selectedAPOD["title"], APODtype=selectedAPOD["media_type"])

        col_l, col_r = st.columns(2)

        with col_l:
            if st.button("Add to favourites", key=f"{selectedAPOD['date']}_fav_selected", use_container_width=True):
                if selectedAPOD not in st.session_state.favorites:
                    st.session_state.favorites.append(selectedAPOD)
                    api_helpers.save_favorites(st.session_state.favorites)
                    st.success("Added to favorites!")
                else:
                    st.info("Already in favorites")

        with col_r:
            if st.button("Details", key=f"{selectedAPOD['date']}_details_selected", use_container_width=True):
                st.session_state.selected_apod = selectedAPOD
                show_details(st.session_state.selected_apod)

    st.divider()

    with st.sidebar:

        st.markdown("# Favorites")

        if "favorites" in st.session_state and len(st.session_state.favorites) > 0:

            favorites = st.session_state.favorites

            for n, fav in enumerate(favorites):

                st.write(f"{n + 1}- {fav['title']}")

                if fav["media_type"] == "image":
                    st.image(fav.get("hdurl") or fav.get("url"))
                else:
                    st.video(fav.get("hdurl") or fav.get("url"))
                
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Show Details", use_container_width=True, key=f"{fav['date']}_detailsShow"):
                        show_details(fav)
                
                with col2:
                    if st.button("Remove", use_container_width=True, key=f"{fav['date']}_remove"):
                        st.session_state.favorites = [f for f in st.session_state.favorites if f['date'] != fav['date']]
                        api_helpers.save_favorites(st.session_state.favorites)
                        st.rerun()

                st.divider()

        else:
            st.info("No favorites saved yet")


@st.dialog("APOD Details", width="large", dismissible=True)
def show_details(data):

    url = data.get('hdurl') or data.get('url')
    response = requests.get(url)
    contents = response.content

    if url:

        if data['media_type'] == "image":
            st.image(url)
            file_name = f"{data['title']}.png"
            mime_type = "image/png"
        else:
            st.video(url)
            file_name = f"{data['title']}.mp4"
            mime_type = "video/mp4"

    else:
        st.error("Error in fetching APOD")
        return

    st.markdown(f"# Title: {data['title']}")
    st.markdown(f"## Date: {data['date']}")

    if data.get('copyright') is not None:
        st.markdown(f"## Copyright: {data['copyright']}")

    st.markdown(f"## URL: {data.get('url')}")
    st.markdown(f"### Explanation: {data['explanation']}")

    st.download_button(
        "Download APOD",
        data=contents,
        file_name=file_name,
        mime=mime_type,
        use_container_width=True
    )


def make_PicCard(data, title, APODtype):
    
    if APODtype == "image":
        st.image(data, caption=f"Title: {title}")
    else:
        st.video(data)


if __name__ == '__main__':
    main()