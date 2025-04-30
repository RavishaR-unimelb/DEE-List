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
df = df.reset_index(drop=True)  # Reset old index
df['Rank'] = df.index + 1
df = df[['Rank', 'Gene', 'Score']]

# --- Page setup ---
st.set_page_config(page_title="Dynamic Search Example", layout="centered")

# --- Search input ---
search_query = st.text_input("Search by gene:")

# --- Filter based on input live ---
if search_query:
    filtered_df = df[df['Gene'].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# --- Show filtered DataFrame ---
st.dataframe(
    filtered_df.style.format({
        "Score": "{:.2f}"
    })
)