import streamlit as st
import pandas as pd
import json

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

# --- Function to filter dataframe based on search query ---
def filter_df():
    search_query = st.session_state.search_query
    if search_query:
        filtered_df = df[df['Gene'].str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df

    # Display filtered dataframe
    st.dataframe(
        filtered_df.style.format({
            "Score": "{:.2f}"
        })
    )

# --- Search bar with on_change callback ---
st.text_input("Search by gene:", key="search_query", on_change=filter_df)

# --- Initial table display (on page load) ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''  # Initialize session state for search query
