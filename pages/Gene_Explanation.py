import streamlit as st
from urllib.parse import parse_qs
import os

# Get query parameters
query_params = st.query_params
gene_name = query_params.get("gene", None)

st.set_page_config(page_title="Explanations Dashboard", layout="centered", initial_sidebar_state="collapsed")

if gene_name:
    #display_name = gene_name.replace('_', ' ')
    display_name = gene_name
    st.title(f"Explanation for {display_name.replace('_', ' ')}")

    image_path = f"images/{display_name}_legend.png"
    if os.path.exists(image_path):
        #st.image(image_path, caption=f"Explanation for {display_name}")
        # --- Layout with two columns ---
        #col1, col2 = st.columns([3, 3])  

        with st.container():
            st.markdown("<div style='display: flex; flex-direction: column; justify-content: flex-start;'>", unsafe_allow_html=True)
            st.image(image_path)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div style='display: flex; flex-direction: column; justify-content: flex-start;'>", unsafe_allow_html=True)
            st.components.v1.html(open(f"images/{display_name}.html", "r").read(), height=800, scrolling=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No image found for this gene.")
else:
    st.error("No gene specified in the URL.")


hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)


