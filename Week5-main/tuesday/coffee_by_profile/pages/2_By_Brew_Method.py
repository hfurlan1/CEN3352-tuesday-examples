import streamlit as st
import pandas as pd

# Configure the page title, icon, and wide layout for this page.
st.set_page_config(page_title="By Brew Method", page_icon="🫗", layout="wide")



@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data



df = load_data()

# Make sure this page still works if someone lands here directly.
if "focus_group_column" not in st.session_state:
    st.session_state.focus_group_column = None
if "focus_group_value" not in st.session_state:
    st.session_state.focus_group_value = None

# Display the page title.
st.title("🫗 By Brew Method")


focus_column = st.session_state.focus_group_column
focus_value = st.session_state.focus_group_value


if focus_column == "brew":
    
    subset = df[df["brew"] == focus_value]
   
    st.caption(f"Showing responses focused on **{focus_value}** (set on Home page).")
else:
    
    subset = df
  
    st.caption("No brew focus group set on Home — showing everyone.")


subset_count = len(subset)

if subset_count == 0:
    
    st.warning("No responses for this group.")
else:
    
    st.write(f"**{subset_count:,}** responses")
    
    st.subheader("Favorite drink")
    
    favorite_counts = subset["favorite"].value_counts()
   
    top_favorites = favorite_counts.head(10)
    
    st.bar_chart(top_favorites)
   
    st.subheader("Self-reported expertise (0-10)")
   
    expertise_counts = subset["expertise"].value_counts()
    
    sorted_expertise_counts = expertise_counts.sort_index()
    
    st.bar_chart(sorted_expertise_counts)
