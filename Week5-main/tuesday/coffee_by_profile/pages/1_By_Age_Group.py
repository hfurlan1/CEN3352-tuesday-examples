import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="By Age Group", page_icon="🎂", layout="wide")


# Load the coffee survey CSV and cache it so it is only read once per session.
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data


# Call the cached loader to get the survey data.
df = load_data()

# Make sure this page still works if someone lands here directly.
if "focus_group_column" not in st.session_state:
    st.session_state.focus_group_column = None
if "focus_group_value" not in st.session_state:
    st.session_state.focus_group_value = None

# Display the page title.
st.title("🎂 By Age Group")


focus_column = st.session_state.focus_group_column
focus_value = st.session_state.focus_group_value

# Check whether the focus group set on Home was based on age.
if focus_column == "age":
    
    subset = df[df["age"] == focus_value]
   
    st.caption(f"Showing responses focused on **{focus_value}** (set on Home page).")
else:
    
    subset = df
    
    st.caption("No age focus group set on Home — showing everyone.")

# Count how many responses are in the subset.
subset_count = len(subset)
# Check whether the subset is empty.
if subset_count == 0:
    
    st.warning("No responses for this group.")
else:
    
    st.write(f"**{subset_count:,}** responses")
    
    st.subheader("Preferred roast level")
    
    roast_counts = subset["roast_level"].value_counts()
    
    st.bar_chart(roast_counts)
   
    st.subheader("Cups per day")
    
    cups_counts = subset["cups"].value_counts()

    st.bar_chart(cups_counts)
