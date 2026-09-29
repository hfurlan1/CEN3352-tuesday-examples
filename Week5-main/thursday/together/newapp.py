import streamlit as st

from importlib import import_module

# The section modules are named with leading digits (1_Compare.py, etc.),
# which isn't a valid Python identifier to import directly - so we load
# them by filename instead and grab each render function off the module.
render_artist_compare = import_module("1_Compare").render_artist_compare
render_discography_explorer = import_module("2_Explorer").render_discography_explorer
render_song_preview = import_module("3_Preview").render_song_preview

# --------------------------------------------------------------------------
# PAGE CONFIG
# Only one st.set_page_config() is allowed per app, and it must be the
# very first Streamlit command that runs. It now covers all three sections.
# --------------------------------------------------------------------------
st.set_page_config(page_title="Music Explorer", page_icon="🎵", layout="wide")

# --------------------------------------------------------------------------
# APP TITLE
# --------------------------------------------------------------------------
st.title("🎵 Music Explorer")
st.markdown(
    "Three mini-apps, one file: search two artists side by side, explore "
    "a discography with a chart, or browse songs with artwork and "
    "previews - all pulling live data from Apple's iTunes Search API."
)

# --------------------------------------------------------------------------
# TOP-LEVEL NAVIGATION
# Each tab just calls the render function for that section - all the
# actual widgets and logic live in 1_Compare.py, 2_Explorer.py, 3_Preview.py.
# --------------------------------------------------------------------------
tab_compare, tab_discography, tab_preview = st.tabs(
    ["🎤 Artist Compare", "🎵 Discography Explorer", "🎧 Song Preview Browser"]
)

with tab_compare:
    render_artist_compare()

with tab_discography:
    render_discography_explorer()

with tab_preview:
    render_song_preview()
