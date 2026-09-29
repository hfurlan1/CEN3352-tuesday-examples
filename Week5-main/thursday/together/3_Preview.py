import streamlit as st
from itunes_api import search_itunes


def render_song_preview():
    """Render the whole Song Preview Browser section: search box + details."""

    # Make sure this section's session_state keys exist before we use them.
    if "browse_term" not in st.session_state:
        st.session_state.browse_term = "BTS"
    if "browse_results" not in st.session_state:
        st.session_state.browse_results = None

    st.header("🎧 Song Preview Browser")
    st.markdown(
        "Same iTunes API, different fields: this section surfaces "
        "`artworkUrl100` and `previewUrl` from the response instead of "
        "just song titles."
    )

    # --- Search box ---
    term = st.text_input(
        "Search", value=st.session_state.browse_term, key="preview_term_input"
    )
    if st.button("Search", key="preview_search_button"):
        st.session_state.browse_term = term
        st.session_state.browse_results = search_itunes(term, entity="song", limit=12)

    st.divider()

    # --- Details, shown once a search has run ---
    results = st.session_state.browse_results
    term = st.session_state.browse_term

    if results is None:
        st.info("Search above to see artwork and previews.")
        return

    result_count = len(results)
    if result_count == 0:
        st.info(f"No songs found for '{term}'.")
        return

    st.caption(f"{result_count} results for '{term}'")

    # Walk through each song one row at a time.
    for row_label in results.index:
        row = results.loc[row_label]
        detail_columns = st.columns([1, 4])

        # Artwork column.
        with detail_columns[0]:
            artwork = row.get("artworkUrl100")
            if isinstance(artwork, str) and artwork:
                st.image(artwork, width=100)
            else:
                st.write("No artwork")

        # Track details column.
        with detail_columns[1]:
            track_name = row.get("trackName", "Unknown")
            st.write(f"**{track_name}**")
            st.write(row.get("collectionName", ""))
            preview = row.get("previewUrl")
            if isinstance(preview, str) and preview:
                st.audio(preview)
            else:
                st.caption("No preview available")

        st.divider()
