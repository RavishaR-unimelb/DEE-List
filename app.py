import streamlit as st
import pandas as pd
import json

# --- Function to filter dataframe based on search query ---
def filter_df():
    search_query = st.session_state.search_query
    if search_query == '':
        filtered_df = df
    else:
        filtered_df = df[df['Gene'].str.contains(search_query, case=False, na=False)]

    # Save the filtered dataframe to session state
    st.session_state.display_df = filtered_df

##################################

# --- Load JSON data ---
with open('prediction_output.json', 'r') as f:
    data = json.load(f)

# --- Prepare the DataFrame ---
df = pd.DataFrame(data['predictions'])

# --- Page setup ---
st.set_page_config(page_title="Predictions Dashboard", layout="centered")

# --- Header ---
st.title("Top DEE Gene Predictions")

# --- Show last updated time ---
st.caption(f"**Last Updated:** {data['updated']}")

##################################

# --- Initialize session state ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''
if 'display_df' not in st.session_state:
    st.session_state.display_df = df

# --- Search bar with on_change callback ---
st.text_input("Search by gene:", key="search_query", on_change=filter_df)

# --- Display dataframe ---
st.dataframe(
    st.session_state.display_df.style.format({
        "Score": "{:.2f}"
    })
)