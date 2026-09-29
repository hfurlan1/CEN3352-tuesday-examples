import streamlit as st
from itunes_api import search_itunes


def render_discography_explorer():
    """Render the whole Discography Explorer section: search box + results."""

    # Make sure this section's session_state keys exist before we use them.
    if "search_term" not in st.session_state:
        st.session_state.search_term = "BTS"
    if "search_results" not in st.session_state:
        st.session_state.search_results = None

    st.header("🎵 Discography Explorer")
    st.markdown(
        "Pulls live song data from Apple's **iTunes Search API** - no CSV, "
        "no key required. Search once, results appear below via "
        "`st.session_state`."
    )

    # --- Search box ---
    term = st.text_input(
        "Search for an artist", value=st.session_state.search_term, key="discography_term_input"
    )
    if st.button("Search", key="discography_search_button"):
        st.session_state.search_term = term
        st.session_state.search_results = search_itunes(term, entity="song", limit=25)

    st.divider()

    # --- Results, shown once a search has run ---
    results = st.session_state.search_results
    term = st.session_state.search_term

    if results is None:
        st.info("Search for an artist above to get started.")
        return

    result_count = len(results)
    if result_count == 0:
        st.warning(f"No songs found for '{term}'. Try another search.")
        return

    st.caption(f"{result_count} results for '{term}'")

    # Table of results, limited to the columns we care about.
    preferred_columns = ["trackName", "collectionName", "artistName", "releaseDate"]
    show_columns = [c for c in preferred_columns if c in results.columns]
    st.dataframe(results[show_columns], use_container_width=True, hide_index=True)

    # Bar chart of songs per album.
    st.subheader("Songs per album (in these results)")
    if "collectionName" in results.columns:
        album_counts = results["collectionName"].value_counts()
        st.bar_chart(album_counts)
