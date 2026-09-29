"""
Small wrapper around Apple's iTunes Search API.

Why this API for a first lesson on pulling from an API:
- No key, no auth, no signup - a plain GET request
- Real, live data (not a static file)
- Simple JSON response that maps directly onto a DataFrame

Rate limit: iTunes allows about 20 requests/minute per IP. st.cache_data
means each unique search only actually hits the network once - repeat
visits (or reruns from unrelated widget interactions) are served from
cache instead of re-fetching.
"""

import requests
import pandas as pd
import streamlit as st

# The base URL for the iTunes Search API.
ITUNES_SEARCH_URL = "https://itunes.apple.com/search"


# Cache each unique search for an hour so reruns do not re-hit the network.
@st.cache_data(ttl=3600, show_spinner="Searching iTunes...")
def search_itunes(term: str, entity: str = "song", limit: int = 25) -> pd.DataFrame:
    """Search the iTunes Store and return results as a DataFrame.

    Returns an empty DataFrame (not an error) when there are no matches,
    so callers can use the same zero-rows pattern as a CSV-based app.
    """
    # Build the query parameters for the request.
    params = {"term": term, "entity": entity, "limit": limit}
    # Send the GET request to the iTunes Search API.
    response = requests.get(ITUNES_SEARCH_URL, params=params, timeout=10)
    # Raise an error if the request failed.
    response.raise_for_status()
    # Parse the JSON response body.
    payload = response.json()
    # Pull out the list of individual results.
    results = payload.get("results", [])
    # Check whether any results came back.
    if not results:
        # Return an empty DataFrame so callers can treat this like the zero-rows case.
        return pd.DataFrame()
    # Convert the list of results into a DataFrame.
    return pd.DataFrame(results)
