import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="Coffee Explorer", page_icon="☕", layout="wide")


# Load the coffee survey CSV and cache it so it is only read once per session.
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data


# Call the cached loader to get the survey data.
df = load_data()

# Check whether a preferred roast has already been stored in session state.
if "preferred_roast" not in st.session_state:
    # Set a default preferred roast the first time this app runs.
    st.session_state.preferred_roast = "All roasts"

# Display the app title.
st.title("☕ Coffee Explorer")
# Explain where the data comes from.
st.markdown(
    "Explore real responses from James Hoffmann's **Great American Coffee "
    "Taste Test** (Oct 2023, ~4,000 participants), via the "
    "[TidyTuesday project](https://github.com/rfordatascience/tidytuesday)."
)

# Draw a horizontal divider line.
st.divider()

# Create three equal-width columns for summary metrics.
columns = st.columns(3)
# Count how many survey responses are in the dataset.
response_count = len(df)
# Show the response count in the first column.
columns[0].metric("Survey responses", f"{response_count:,}")
# Count how many columns are in the dataset.
column_count = df.shape[1]
# Show the column count in the second column.
columns[1].metric("Columns kept", f"{column_count}")
# Get the roast_level column on its own.
roast_level_column = df["roast_level"]
# Find which rows are missing a roast_level value.
missing_roast_flags = roast_level_column.isna()
# Count how many rows are missing a roast_level value.
missing_roast_count = missing_roast_flags.sum()
# Show the missing-value count in the third column.
columns[2].metric("Missing roast_level", f"{missing_roast_count:,}")

# Draw another horizontal divider line.
st.divider()

# Display a subheader introducing the roast picker.
st.subheader("Pick a roast to follow you to the Explore Data page")
# Get the roast_level column without missing values.
known_roasts = df["roast_level"].dropna()
# Get the unique roast levels present in the data.
unique_roasts = known_roasts.unique()
# Sort the unique roast levels alphabetically.
sorted_roasts = sorted(unique_roasts)
# Build the full list of dropdown options, starting with "All roasts".
roast_options = ["All roasts"] + sorted_roasts

# Read the roast currently stored in session state.
current_roast = st.session_state.preferred_roast
# Work out which option should be pre-selected in the dropdown.
if current_roast in roast_options:
    # Use the position of the stored roast as the default index.
    default_index = roast_options.index(current_roast)
else:
    # Fall back to the first option if the stored roast is no longer valid.
    default_index = 0

# Show the roast selector, pre-selected to the current session state value.
choice = st.selectbox("Preferred roast", roast_options, index=default_index)
# Save the chosen roast back into session state so other pages can read it.
st.session_state.preferred_roast = choice

# Confirm the current selection and explain what happens next.
st.info(
    f"Currently set to **{st.session_state.preferred_roast}**. "
    "Open **Explore Data** in the sidebar — the table there starts "
    "pre-filtered to this roast, because it reads the same "
    "`st.session_state.preferred_roast` value."
)

# Remind the visitor how to navigate to the other pages.
st.caption("Use the sidebar to navigate to Explore Data or About.")
