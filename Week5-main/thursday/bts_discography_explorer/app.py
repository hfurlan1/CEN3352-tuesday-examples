import streamlit as st
from itunes_api import search_itunes

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="BTS Discography Explorer", page_icon="🎵", layout="wide")

# Check whether a search term has already been stored in session state.
if "search_term" not in st.session_state:
    # Default the search term to BTS the first time this app runs.
    st.session_state.search_term = "BTS"
# Check whether search results have already been stored in session state.
if "search_results" not in st.session_state:
    # No search has happened yet.
    st.session_state.search_results = None

# Display the app title.
st.title("🎵 Discography Explorer")
# Explain what this app does and where the data comes from.
st.markdown(
    "Pulls live song data from Apple's **iTunes Search API** - no CSV, "
    "no key required. Search once here; the results follow you to the "
    "Results page via `st.session_state`."
)

# Show a text input pre-filled with the current search term.
term = st.text_input("Search for an artist", value=st.session_state.search_term)

# Check whether the visitor pressed the Search button.
if st.button("Search"):
    # Save the search term into session state.
    st.session_state.search_term = term
    # Run the search and save the results into session state.
    st.session_state.search_results = search_itunes(term, entity="song", limit=25)

# Check whether a search has been run yet.
if st.session_state.search_results is not None:
    # Count how many songs came back.
    result_count = len(st.session_state.search_results)
    # Check whether the search returned zero songs.
    if result_count == 0:
        # Warn the visitor that nothing matched.
        st.warning(
            f"No songs found for '{st.session_state.search_term}'. "
            "Try another search."
        )
    else:
        # Confirm the search succeeded and point to the Results page.
        st.success(
            f"Found {result_count} songs for '{st.session_state.search_term}'. "
            "See the Results page."
        )
else:
    # Prompt the visitor to run a first search.
    st.info("Search for an artist to get started.")
