import streamlit as st
from itunes_api import search_itunes

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="Artist Compare", page_icon="🎤", layout="wide")

# Check whether the first artist's data has already been stored.
if "artist_1_name" not in st.session_state:
    st.session_state.artist_1_name = None
if "artist_1_results" not in st.session_state:
    st.session_state.artist_1_results = None
# Check whether the second artist's data has already been stored.
if "artist_2_name" not in st.session_state:
    st.session_state.artist_2_name = None
if "artist_2_results" not in st.session_state:
    st.session_state.artist_2_results = None

# Display the app title.
st.title("🎤 Artist Compare")
# Explain what this app does.
st.markdown(
    "Search two artists via the iTunes API; each search is cached and "
    "held in `st.session_state` so the Compare page can show both "
    "side by side without re-fetching."
)

# Create two equal-width columns, one per artist.
columns = st.columns(2)

# Build the first artist's search box inside the first column.
with columns[0]:
    # Show a text input for the first artist's name.
    name1 = st.text_input("Artist 1", value="BTS")
    # Check whether the visitor pressed the search button for artist 1.
    if st.button("Search artist 1"):
        # Save the artist's name into session state.
        st.session_state.artist_1_name = name1
        # Run the search and save the results into session state.
        st.session_state.artist_1_results = search_itunes(
            name1, entity="song", limit=15
        )

# Build the second artist's search box inside the second column.
with columns[1]:
    # Show a text input for the second artist's name.
    name2 = st.text_input("Artist 2", value="Coldplay")
    # Check whether the visitor pressed the search button for artist 2.
    if st.button("Search artist 2"):
        # Save the artist's name into session state.
        st.session_state.artist_2_name = name2
        # Run the search and save the results into session state.
        st.session_state.artist_2_results = search_itunes(
            name2, entity="song", limit=15
        )

# Check whether both artists have been searched.
artist_1_ready = st.session_state.artist_1_results is not None
artist_2_ready = st.session_state.artist_2_results is not None
if artist_1_ready and artist_2_ready:
    # Both searches are done, so point the visitor to the Compare page.
    st.success("Both artists searched — see the Compare page.")
else:
    # At least one search is still missing.
    st.info("Search both artists to enable the comparison.")
