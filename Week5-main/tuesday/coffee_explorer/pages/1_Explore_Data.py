import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Explore Data", page_icon="🔍", layout="wide")


# Load the coffee survey CSV and cache it so it is only read once per session.
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data


# Call the cached loader to get the survey data.
df = load_data()

# Make sure this page still works if someone lands here directly
# (e.g. a bookmark) without visiting Home first.
if "preferred_roast" not in st.session_state:
    # Set the same default roast used on the Home page.
    st.session_state.preferred_roast = "All roasts"

# Display the page title.
st.title("🔍 Explore Data")
# Explain that the roast filter carried over from the Home page.
st.caption(
    f"Pre-filtered to **{st.session_state.preferred_roast}** — "
    "this came from the Home page's session state, not a fresh choice."
)

# Get the roast_level column without missing values.
known_roasts = df["roast_level"].dropna()
# Get the unique roast levels present in the data.
unique_roasts = known_roasts.unique()
# Sort the unique roast levels alphabetically.
sorted_roasts = sorted(unique_roasts)
# Build the full list of roast dropdown options.
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
roast = st.selectbox(
    "Roast level", roast_options, index=default_index, key="roast_selectbox"
)
# Save the chosen roast back into session state so it persists across reruns.
st.session_state.preferred_roast = roast

# Get the age column without missing values.
known_ages = df["age"].dropna()
# Get the unique age groups present in the data.
unique_ages = known_ages.unique()
# Sort the unique age groups alphabetically.
sorted_ages = sorted(unique_ages)
# Build the full list of age dropdown options.
age_options = ["All ages"] + sorted_ages
# Show the age selector.
age = st.selectbox("Age group", age_options)

# Start with a copy of the full dataset before filtering.
filtered = df.copy()
# Apply the roast filter if a specific roast was chosen.
if roast != "All roasts":
    filtered = filtered[filtered["roast_level"] == roast]
# Apply the age filter if a specific age group was chosen.
if age != "All ages":
    filtered = filtered[filtered["age"] == age]

# Count how many rows matched both filters.
matching_count = len(filtered)
# Show the number of matching responses.
st.write(f"**{matching_count:,}** matching responses")

# Check whether any rows matched the filters.
if matching_count == 0:
    # Warn the visitor that the filter combination returned nothing.
    st.warning("No responses match that combination. Try a broader filter.")
else:
    # List the columns to show in the results table.
    display_columns = [
        "age",
        "cups",
        "brew",
        "favorite",
        "roast_level",
        "strength",
        "expertise",
    ]
    # Show the filtered responses as a table.
    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    # Display a subheader for the favorite-drink chart.
    st.subheader("Favorite drink, by count")
    # Count how many times each favorite drink appears.
    favorite_counts = filtered["favorite"].value_counts()
    # Keep only the top ten favorite drinks.
    top_favorites = favorite_counts.head(10)
    # Show the counts as a bar chart.
    st.bar_chart(top_favorites)
