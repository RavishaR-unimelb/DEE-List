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

# --- Search bar ---
search_query = st.text_input("Search by gene:", key="search")

# --- Filter DataFrame based on search ---
if search_query:
    filtered_df = df[df['Gene'].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# --- Display the table ---
st.dataframe(
    filtered_df.style.format({
        "Score": "{:.2f}"
    })
)
