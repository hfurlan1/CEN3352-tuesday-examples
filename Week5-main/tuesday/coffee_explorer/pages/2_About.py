import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About this app")

st.markdown(
    """
This app explores the **Great American Coffee Taste Test** dataset.

**Where the data comes from**
In October 2023, coffee educator James Hoffmann and coffee company
Cometeer ran a live-streamed blind taste test. Roughly 4,000 viewers
tasted four unlabeled coffees at home and filled out a survey on their
preferences, brewing habits, and demographics. The cleaned dataset is
published through the
[TidyTuesday project](https://github.com/rfordatascience/tidytuesday/blob/main/data/2024/2024-05-14/readme.md).

**What this app demonstrates**
- A multi-page Streamlit app using the `pages/` folder convention
- Passing a value (`preferred_roast`) across pages with `st.session_state`
- Filtering and displaying real survey data

**Pages**
- **Home** — pick a preferred roast
- **Explore Data** — filter and chart survey responses
- **About** — this page
"""
)
