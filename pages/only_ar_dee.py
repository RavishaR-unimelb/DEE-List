import streamlit as st
import pandas as pd
import json

# --- Page config ---
st.set_page_config(page_title="Only AR DEE Predictions", layout="centered")

# --- Header ---
st.title("DEE Gene Predictions: Only AR Genes")

# --- Load JSON data (or however you structure it) ---
with open('prediction_output.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data['predictions'])
df = df.reset_index(drop=True)
df['Rank'] = df.index + 1
df = df[['Rank', 'Gene', 'Score']]

# --- Optional: Search ---
search_query = st.text_input("Search by gene (AR set):", '')
if search_query:
    df = df[df['Gene'].str.contains(search_query, case=False, na=False)]

# --- Display results ---
st.dataframe(
    df.style.format({"Score": "{:.2f}"}).hide(axis="index")
)

# --- Show last updated info ---
st.caption(f"**Last Updated:** {data['updated']}")
