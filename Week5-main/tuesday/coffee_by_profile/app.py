import streamlit as st
import pandas as pd


st.set_page_config(page_title="Coffee by Profile", page_icon="👥", layout="wide")



@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame.
    data = pd.read_csv("coffee_survey.csv")
    # Return the DataFrame to the caller.
    return data



df = load_data()


if "focus_group_column" not in st.session_state:
    # No column has been chosen yet.
    st.session_state.focus_group_column = None
if "focus_group_value" not in st.session_state:
    # No value has been chosen yet.
    st.session_state.focus_group_value = None


st.title("👥 Coffee by Profile")

st.markdown(
    "This app slices the same coffee taste-test data by **who's drinking**, "
    "not by which coffee. Pick a group below; every other page narrows to it."
)

# Draw a horizontal divider line.
st.divider()
# Display a subheader introducing the focus-group picker.
st.subheader("Choose a focus group")


group_type = st.radio("Slice by", ["Age group", "Brew method"], horizontal=True)


if group_type == "Age group":
    
    known_ages = df["age"].dropna()
   
    unique_ages = known_ages.unique()
   
    options = sorted(unique_ages)
    
    picked = st.selectbox("Age group", options)
    
    if st.button("Set as focus group"):
        st.session_state.focus_group_column = "age"
        st.session_state.focus_group_value = picked
else:
    
    known_brews = df["brew"].dropna()
  
    unique_brews = known_brews.unique()
    
    options = sorted(unique_brews)
    
    picked = st.selectbox("Brew method", options)
   
    if st.button("Set as focus group"):
        st.session_state.focus_group_column = "brew"
        st.session_state.focus_group_value = picked


if st.session_state.focus_group_column is not None:
    
    focus_column = st.session_state.focus_group_column
    focus_value = st.session_state.focus_group_value
    
    st.success(
        f"Focus group set: **{focus_column} = {focus_value}**. "
        "Check By Age Group or By Brew Method."
    )
else:
   
    st.info("No focus group set yet — the other pages will show everyone.")
