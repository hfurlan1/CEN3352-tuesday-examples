import streamlit as st

st.set_page_config(page_title="Methodology", page_icon="📋", layout="wide")

st.title("📋 Methodology")

st.markdown(
    """
**Data source:** [Great American Coffee Taste Test](https://github.com/rfordatascience/tidytuesday/blob/main/data/2024/2024-05-14/readme.md)
(TidyTuesday, 2024-05-14), originally collected by James Hoffmann and
Cometeer in October 2023.

**How the tasting worked:** ~4,000 participants each received four
unlabeled coffee samples (Coffee A-D) shipped by Cometeer, tasted them
along with a livestream, and rated each one from 1 (dislike) to 5 (like)
on personal preference, along with bitterness and acidity.

**This app's page structure (task-based):**
- **Rankings** — overall standings across all ~4,000 tasters
- **Compare Two Coffees** — pick any two coffees for a head-to-head look
- **Methodology** — this page

This is a different page-splitting philosophy than *Coffee Explorer*
(page-per-dataset-view) or *Coffee by Profile* (page-per-demographic-slice) —
here, each page is a different **task** a user might want to do.
"""
)
