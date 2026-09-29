import streamlit as st

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Details", page_icon="🖼️", layout="wide")

# Display the page title.
st.title("🖼️ Details")

# Read the browse results and browse term out of session state.
results = st.session_state.get("browse_results")
term = st.session_state.get("browse_term", "")

# Make sure a search has already been run before showing details.
if results is None:
    # Tell the visitor to search first, then stop rendering this page.
    st.warning("No search yet - go to the Search page first.")
    st.stop()

# Count how many results came back.
result_count = len(results)
# Check whether the search returned zero songs.
if result_count == 0:
    # Tell the visitor nothing matched, then stop rendering this page.
    st.info(f"No songs found for '{term}'.")
    st.stop()

# Show how many results are being displayed.
st.caption(f"{result_count} results for '{term}'")

# Get the row labels so each row can be looked up one at a time.
row_labels = results.index
# Walk through the results one row at a time, in order.
for row_label in row_labels:
    # Look up the full row for this label.
    row = results.loc[row_label]
    # Create a narrow column for artwork and a wide column for details.
    columns = st.columns([1, 4])
    # Fill in the artwork column.
    with columns[0]:
        # Get the artwork URL for this song.
        artwork = row.get("artworkUrl100")
        # Check whether a usable artwork URL is present.
        if isinstance(artwork, str) and artwork:
            # Show the artwork image.
            st.image(artwork, width=100)
        else:
            # Let the visitor know there is no artwork to show.
            st.write("No artwork")
    # Fill in the details column.
    with columns[1]:
        # Get the track name for this song.
        track_name = row.get("trackName", "Unknown")
        # Show the track name in bold.
        st.write(f"**{track_name}**")
        # Get the album name for this song.
        album_name = row.get("collectionName", "")
        # Show the album name.
        st.write(album_name)
        # Get the preview URL for this song.
        preview = row.get("previewUrl")
        # Check whether a usable preview URL is present.
        if isinstance(preview, str) and preview:
            # Play the audio preview.
            st.audio(preview)
        else:
            # Let the visitor know there is no preview to play.
            st.caption("No preview available")
    # Draw a divider between songs.
    st.divider()
