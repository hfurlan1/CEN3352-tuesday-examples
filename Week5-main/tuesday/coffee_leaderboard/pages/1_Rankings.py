import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="Rankings", page_icon="📊", layout="wide")


# Load the coffee survey CSV and cache it so it is only read once per session.
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data


# Call the cached loader to get the survey data.
df = load_data()

# Display the page title.
st.title("📊 Rankings")
# Explain what the chart below shows.
st.caption("Average personal-preference score (1-5) for each blind-tasted coffee.")

# Calculate the average personal-preference score for each coffee, one at a time.
avg_a = df["coffee_a_personal_preference"].mean()
avg_b = df["coffee_b_personal_preference"].mean()
avg_c = df["coffee_c_personal_preference"].mean()
avg_d = df["coffee_d_personal_preference"].mean()

# Build a Series that maps each coffee name to its average score.
avg_series = pd.Series(
    {
        "Coffee A": avg_a,
        "Coffee B": avg_b,
        "Coffee C": avg_c,
        "Coffee D": avg_d,
    }
)
# Sort the coffees from highest average score to lowest.
avg_series_sorted = avg_series.sort_values(ascending=False)

# Show the sorted averages as a bar chart.
st.bar_chart(avg_series_sorted)

# Display a subheader for the table view.
st.subheader("As a table")
# Round the averages to two decimal places.
rounded_series = avg_series_sorted.round(2)
# Name the series values column before turning it into a table.
named_series = rounded_series.rename("Average preference (1-5)")
# Convert the series into a two-column DataFrame.
avg_table = named_series.reset_index()
# Rename the index column so it reads "Coffee" instead of "index".
avg_table = avg_table.rename(columns={"index": "Coffee"})
# Show the table of average scores.
st.dataframe(avg_table, use_container_width=True, hide_index=True)
