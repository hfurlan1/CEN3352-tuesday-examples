import streamlit as st
from itunes_api import search_itunes

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="Song Preview Browser", page_icon="🎧", layout="wide")

# Check whether browse results have already been stored in session state.
if "browse_results" not in st.session_state:
    st.session_state.browse_results = None
# Check whether a browse term has already been stored in session state.
if "browse_term" not in st.session_state:
    st.session_state.browse_term = "BTS"

# Display the app title.
st.title("🎧 Song Preview Browser")
# Explain what makes this app different from the other iTunes apps.
st.markdown(
    "Same iTunes API, different fields: this app surfaces `artworkUrl100` "
    "and `previewUrl` from the response instead of just song titles."
)

# Show a text input pre-filled with the current search term.
term = st.text_input("Search", value=st.session_state.browse_term)
# Check whether the visitor pressed the Search button.
if st.button("Search"):
    # Save the search term into session state.
    st.session_state.browse_term = term
    # Run the search and save the results into session state.
    st.session_state.browse_results = search_itunes(term, entity="song", limit=12)

# Point the visitor to the Details page to see artwork and previews.
st.caption("See the Details page for artwork and previews.")
