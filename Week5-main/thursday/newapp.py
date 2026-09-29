import streamlit as st
from itunes_api import search_itunes

# --------------------------------------------------------------------------
# PAGE CONFIG
# Only one st.set_page_config() is allowed per app, and it must be the
# very first Streamlit command that runs. It now covers all three sections.
# --------------------------------------------------------------------------
st.set_page_config(page_title="Music Explorer", page_icon="🎵", layout="wide")

# --------------------------------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------------------------------

# Initialize the authenticated flag the first time the app runs in a session.
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Initialize the username the first time the app runs in a session.
if "username" not in st.session_state:
    st.session_state["username"] = None

# If the visitor is NOT authenticated yet, show only the login form and
# stop the script right there - st.stop() prevents every line below it
# from running, which is what actually keeps the rest of the app hidden.
if st.session_state["authenticated"] == False:
    st.title("🎵 Music Explorer")
    st.caption("Please log in to continue.")

    # st.form groups the two inputs and the submit button so the app only reruns once, on submit.
    login_form = st.form("login_form")

    # Add the username field inside the form.
    entered_username = login_form.text_input("Username")

    # Add the password field inside the form. type="password" masks the characters as they are typed.
    entered_password = login_form.text_input("Password", type="password")

    # Add the submit button inside the form.
    submitted = login_form.form_submit_button("Log in")

    # Only check credentials after the form has been submitted.
    if submitted == True:
        # Read the correct username out of secrets.toml.
        correct_username = st.secrets["credentials"]["username"]
        # Read the correct password out of secrets.toml.
        correct_password = st.secrets["credentials"]["password"]

        # Compare the entered credentials against the ones in secrets.toml.
        username_matches = entered_username == correct_username
        password_matches = entered_password == correct_password

        # Both fields must match before access is granted.
        if username_matches and password_matches:
            st.session_state["authenticated"] = True
            st.session_state["username"] = entered_username
            # Rerun so the rest of the app replaces the form immediately.
            st.rerun()
        else:
            st.error("Incorrect username or password.")

    # Stop here so nothing below (the tabs, the app itself) renders
    # while the visitor is still logged out.
    st.stop()

# From this point on, the visitor is authenticated. Show who's logged in
# and give them a way to log back out.
st.sidebar.success(f"Logged in as {st.session_state['username']}")
if st.sidebar.button("Log out"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()

# --------------------------------------------------------------------------
# SESSION STATE
# Each of the three original apps kept its own set of session_state keys.
# We keep those same keys (they don't collide with each other) and make
# sure they all exist before anything tries to read them.
# --------------------------------------------------------------------------
default_state = {
    # Artist Compare section
    "artist_1_name": None,
    "artist_1_results": None,
    "artist_2_name": None,
    "artist_2_results": None,
    # Discography Explorer section
    "search_term": "BTS",
    "search_results": None,
    # Song Preview Browser section
    "browse_term": "BTS",
    "browse_results": None,
}
for key, default_value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# ==========================================================================
# PAGE 1: ARTIST COMPARE
# Combines artist_compare/app.py (search) + pages/1_Compare.py (comparison)
# ==========================================================================
def page_artist_compare():
    st.title("🎤 Artist Compare")
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
    else:
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


# ==========================================================================
# PAGE 2: DISCOGRAPHY EXPLORER
# Combines bts_discography_explorer/app.py (search) + pages/1_Results.py
# ==========================================================================
def page_discography_explorer():
    st.title("🎵 Discography Explorer")
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
    else:
        result_count = len(results)
        if result_count == 0:
            st.warning(f"No songs found for '{term}'. Try another search.")
        else:
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


# ==========================================================================
# PAGE 3: SONG PREVIEW BROWSER
# Combines song_preview_browser/app.py (search) + pages/1_Details.py
# ==========================================================================
def page_song_preview():
    st.title("🎧 Song Preview Browser")
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
    else:
        result_count = len(results)
        if result_count == 0:
            st.info(f"No songs found for '{term}'.")
        else:
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


# --------------------------------------------------------------------------
# TOP-LEVEL NAVIGATION
# st.navigation() + st.Page() replace st.tabs(): each section becomes its
# own real page with its own sidebar entry and URL, instead of a tab
# stacked next to the others. Streamlit only draws the sidebar nav list
# and the current page's title bar - the rest is exactly what
# page.run() calls, i.e. one of the three functions defined above.
# --------------------------------------------------------------------------
pages = [
    st.Page(page_artist_compare, title="Artist Compare", icon="🎤"),
    st.Page(page_discography_explorer, title="Discography Explorer", icon="🎵"),
    st.Page(page_song_preview, title="Song Preview Browser", icon="🎧"),
]
current_page = st.navigation(pages)
current_page.run()
