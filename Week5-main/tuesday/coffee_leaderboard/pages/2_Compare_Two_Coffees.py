import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Compare Two Coffees", page_icon="⚖️", layout="wide")

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

# Make sure this page still works if someone lands here directly.
if "compare_left" not in st.session_state:
    st.session_state.compare_left = "A"
if "compare_right" not in st.session_state:
    st.session_state.compare_right = "B"

# Display the page title.
st.title("⚖️ Compare Two Coffees")

# Read the current comparison pair from session state.
left = st.session_state.compare_left
right = st.session_state.compare_right
# Show which coffees are currently being compared.
st.caption(f"Comparing Coffee {left} vs Coffee {right} (set on Home page).")

# Create two equal-width columns for the two selectors.
columns = st.columns(2)
# Find the current left-hand coffee's position in the coffee list.
left_index = COFFEES.index(left)
# Show the left-hand coffee selector in the first column.
new_left = columns[0].selectbox("Coffee 1", COFFEES, index=left_index, key="cmp_left")
# Find the current right-hand coffee's position in the coffee list.
right_index = COFFEES.index(right)
# Show the right-hand coffee selector in the second column.
new_right = columns[1].selectbox(
    "Coffee 2", COFFEES, index=right_index, key="cmp_right"
)

# Save both selections back into session state.
st.session_state.compare_left = new_left
st.session_state.compare_right = new_right
# Use the freshly selected coffees for the rest of this page.
left = new_left
right = new_right

# Build the personal-preference column name for the left-hand coffee.
left_column_name = f"coffee_{left.lower()}_personal_preference"
# Build the personal-preference column name for the right-hand coffee.
right_column_name = f"coffee_{right.lower()}_personal_preference"

# Calculate the average preference score for the left-hand coffee.
avg_left = df[left_column_name].mean()
# Calculate the average preference score for the right-hand coffee.
avg_right = df[right_column_name].mean()

# Create two equal-width columns for the two average-score metrics.
metric_columns = st.columns(2)
# Show the left-hand coffee's average score.
metric_columns[0].metric(f"Coffee {left} avg preference", f"{avg_left:.2f}")
# Show the right-hand coffee's average score.
metric_columns[1].metric(f"Coffee {right} avg preference", f"{avg_right:.2f}")

# Get the raw preference scores for the left-hand coffee.
left_scores = df[left_column_name]
# Get the raw preference scores for the right-hand coffee.
right_scores = df[right_column_name]
# Combine both score columns into one comparison DataFrame.
compare_df = pd.DataFrame(
    {
        f"Coffee {left}": left_scores,
        f"Coffee {right}": right_scores,
    }
)

# Display a subheader for the distribution chart.
st.subheader("Preference score distribution (1-5)")
# Count how many times each score (1-5) appears for each coffee.
left_score_counts = left_scores.value_counts()
right_score_counts = right_scores.value_counts()
# Combine the two count Series into one DataFrame, aligned by score.
score_counts_df = pd.DataFrame(
    {
        f"Coffee {left}": left_score_counts,
        f"Coffee {right}": right_score_counts,
    }
)
# Sort the rows by score value so the chart reads 1 through 5 in order.
sorted_score_counts_df = score_counts_df.sort_index()
# Show the score distributions as a bar chart.
st.bar_chart(sorted_score_counts_df)
