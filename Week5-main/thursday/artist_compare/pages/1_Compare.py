import streamlit as st

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Compare", page_icon="⚖️", layout="wide")

# Display the page title.
st.title("⚖️ Compare")

# Read both artists' names and results out of session state.
name1 = st.session_state.get("artist_1_name")
results1 = st.session_state.get("artist_1_results")
name2 = st.session_state.get("artist_2_name")
results2 = st.session_state.get("artist_2_results")

# Make sure both artists have been searched before showing a comparison.
if not name1 or not name2:
    # Tell the visitor to search first, then stop rendering this page.
    st.warning("Search both artists on the Home page first.")
    st.stop()

# List the preferred columns to display, in order of preference.
preferred_columns = ["trackName", "collectionName"]

# Create two equal-width columns, one per artist.
columns = st.columns(2)

# Build the first artist's summary inside the first column.
with columns[0]:
    # Show the artist's name as a subheader.
    st.subheader(name1)
    # Count how many songs came back for this artist.
    result_count = len(results1)
    if result_count == 0:
        # Tell the visitor nothing matched for this artist.
        st.info(f"No songs found for '{name1}'.")
    else:
        # Show the number of songs found.
        st.metric("Songs found", result_count)
        # Check whether an album column is present before counting albums.
        if "collectionName" in results1.columns:
            # Count how many distinct albums are represented.
            album_count = results1["collectionName"].nunique()
            # Show the album count.
            st.write("Albums represented:", album_count)
        # Keep only the preferred columns that are actually present.
        show_columns = []
        for column_name in preferred_columns:
            if column_name in results1.columns:
                show_columns.append(column_name)
        # Show the results table with just the chosen columns.
        st.dataframe(results1[show_columns], use_container_width=True, hide_index=True)

# Build the second artist's summary inside the second column.
with columns[1]:
    # Show the artist's name as a subheader.
    st.subheader(name2)
    # Count how many songs came back for this artist.
    result_count = len(results2)
    if result_count == 0:
        # Tell the visitor nothing matched for this artist.
        st.info(f"No songs found for '{name2}'.")
    else:
        # Show the number of songs found.
        st.metric("Songs found", result_count)
        # Check whether an album column is present before counting albums.
        if "collectionName" in results2.columns:
            # Count how many distinct albums are represented.
            album_count = results2["collectionName"].nunique()
            # Show the album count.
            st.write("Albums represented:", album_count)
        # Keep only the preferred columns that are actually present.
        show_columns = []
        for column_name in preferred_columns:
            if column_name in results2.columns:
                show_columns.append(column_name)
        # Show the results table with just the chosen columns.
        st.dataframe(results2[show_columns], use_container_width=True, hide_index=True)
