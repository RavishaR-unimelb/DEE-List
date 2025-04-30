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
st.title("Predictions Overview")

# --- Show last updated time ---
st.caption(f"**Last Updated:** {data['updated']}")

# --- Display the table ---
st.dataframe(
    df.style.format({
        "confidence": "{:.2f}"
    }).background_gradient(subset=['confidence'], cmap='Greens')
)
