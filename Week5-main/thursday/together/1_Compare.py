import streamlit as st
from itunes_api import search_itunes


def render_artist_compare():
    """Render the whole Artist Compare section: search boxes + comparison."""

    # Make sure this section's session_state keys exist before we use them.
    for key in ["artist_1_name", "artist_1_results", "artist_2_name", "artist_2_results"]:
        if key not in st.session_state:
            st.session_state[key] = None

    st.header("🎤 Artist Compare")
    st.markdown(
        "Search two artists via the iTunes API; each search is cached and "
        "held in `st.session_state` so the comparison below can show both "
        "side by side without re-fetching."
    )

    # --- Search boxes for both artists, side by side ---
    search_columns = st.columns(2)

    with search_columns[0]:
        name1 = st.text_input("Artist 1", value="BTS", key="compare_name1_input")
        if st.button("Search artist 1"):
            st.session_state.artist_1_name = name1
            st.session_state.artist_1_results = search_itunes(
                name1, entity="song", limit=15
            )

    with search_columns[1]:
        name2 = st.text_input("Artist 2", value="Coldplay", key="compare_name2_input")
        if st.button("Search artist 2"):
            st.session_state.artist_2_name = name2
            st.session_state.artist_2_results = search_itunes(
                name2, entity="song", limit=15
            )

    st.divider()

    # --- Comparison, shown once both artists have been searched ---
    name1 = st.session_state.artist_1_name
    results1 = st.session_state.artist_1_results
    name2 = st.session_state.artist_2_name
    results2 = st.session_state.artist_2_results

    if not name1 or not name2:
        # At least one artist hasn't been searched yet - nothing to compare.
        st.info("Search both artists above to see the comparison.")
        return

    st.subheader("⚖️ Comparison")

    # Columns we'd like to show, in order of preference.
    preferred_columns = ["trackName", "collectionName"]

    compare_columns = st.columns(2)

    # Build the first artist's summary.
    with compare_columns[0]:
        st.subheader(name1)
        result_count = len(results1)
        if result_count == 0:
            st.info(f"No songs found for '{name1}'.")
        else:
            st.metric("Songs found", result_count)
            if "collectionName" in results1.columns:
                album_count = results1["collectionName"].nunique()
                st.write("Albums represented:", album_count)
            show_columns = [c for c in preferred_columns if c in results1.columns]
            st.dataframe(results1[show_columns], use_container_width=True, hide_index=True)

    # Build the second artist's summary.
    with compare_columns[1]:
        st.subheader(name2)
        result_count = len(results2)
        if result_count == 0:
            st.info(f"No songs found for '{name2}'.")
        else:
            st.metric("Songs found", result_count)
            if "collectionName" in results2.columns:
                album_count = results2["collectionName"].nunique()
                st.write("Albums represented:", album_count)
            show_columns = [c for c in preferred_columns if c in results2.columns]
            st.dataframe(results2[show_columns], use_container_width=True, hide_index=True)
