import streamlit as st
import requests

RAW_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/prediction-streamlit-app/main/prediction_output.json"

st.title("ML Prediction Viewer")

try:
    response = requests.get(RAW_URL)
    response.raise_for_status()
    data = response.json()
    
    st.markdown(f"**Last Updated:** `{data['updated']}`")
    st.write("### Predictions")
    st.json(data['predictions'])

except Exception as e:
    st.error(f"Failed to fetch predictions: {e}")
