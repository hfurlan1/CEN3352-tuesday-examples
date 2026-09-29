import streamlit as st

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Results", page_icon="📄", layout="wide")

# Display the page title.
st.title("📄 Results")

# Make sure a search has already been run before showing results.
if "search_results" not in st.session_state or st.session_state.search_results is None:
    # Tell the visitor to search first, then stop rendering this page.
    st.warning("No search yet - go to the Search page first.")
    st.stop()

# Read the search results and search term out of session state.
results = st.session_state.search_results
term = st.session_state.get("search_term", "")

# Count how many results came back.
result_count = len(results)
# Check whether the search returned zero songs.
if result_count == 0:
    # Tell the visitor nothing matched, then stop rendering this page.
    st.info(f"No songs found for '{term}'.")
    st.stop()

# Show how many results matched and where they came from.
st.caption(
    f"{result_count} results for '{term}' - fetched once on the Search "
    "page, reused here from `st.session_state` (no re-fetch)."
)

# List the columns we want to show, in order of preference.
preferred_columns = ["trackName", "collectionName", "artistName", "releaseDate"]
# Keep only the preferred columns that are actually present in the results.
show_columns = []
for column_name in preferred_columns:
    if column_name in results.columns:
        show_columns.append(column_name)

# Show the results table with just the chosen columns.
st.dataframe(results[show_columns], use_container_width=True, hide_index=True)

# Display a subheader for the per-album chart.
st.subheader("Songs per album (in these results)")
# Check whether an album column is present before charting it.
if "collectionName" in results.columns:
    # Count how many songs belong to each album.
    album_counts = results["collectionName"].value_counts()
    # Show the album counts as a bar chart.
    st.bar_chart(album_counts)
