import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this app.
st.set_page_config(page_title="Coffee Leaderboard", page_icon="🏆", layout="wide")

# List the coffee labels used throughout this app.
COFFEES = ["A", "B", "C", "D"]


# Load the coffee survey CSV and cache it so it is only read once per session.
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data


# Call the cached loader to get the survey data.
df = load_data()

# Check whether a comparison pair has already been stored in session state.
if "compare_left" not in st.session_state:
    # Default the left-hand coffee to A.
    st.session_state.compare_left = "A"
if "compare_right" not in st.session_state:
    # Default the right-hand coffee to B.
    st.session_state.compare_right = "B"

# Display the app title.
st.title("🏆 Coffee Leaderboard")
# Explain what this app does.
st.markdown(
    "Same dataset, organized by **task** instead of by data slice: "
    "Rankings, a head-to-head Compare page, and Methodology."
)

# Draw a horizontal divider line.
st.divider()
# Display a subheader introducing the comparison picker.
st.subheader("Set up your head-to-head comparison")

# Create two equal-width columns for the two selectors.
columns = st.columns(2)
# Find the current left-hand coffee's position in the coffee list.
left_index = COFFEES.index(st.session_state.compare_left)
# Show the left-hand coffee selector in the first column.
left = columns[0].selectbox("Coffee 1", COFFEES, index=left_index)
# Find the current right-hand coffee's position in the coffee list.
right_index = COFFEES.index(st.session_state.compare_right)
# Show the right-hand coffee selector in the second column.
right = columns[1].selectbox("Coffee 2", COFFEES, index=right_index)

# Save both selections back into session state.
st.session_state.compare_left = left
st.session_state.compare_right = right

# Tell the visitor where to go to see the comparison.
st.info(f"Go to **Compare Two Coffees** to see Coffee {left} vs Coffee {right}.")
