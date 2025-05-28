import streamlit as st
from urllib.parse import parse_qs
import os

# Get query parameters
query_params = st.query_params
gene_name = query_params.get("gene", None)

st.set_page_config(page_title="Explanations Dashboard", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .element-container {
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

if gene_name:
    #display_name = gene_name.replace('_', ' ')
    display_name = gene_name
    st.title(f"Explanation for {display_name.replace('_', ' ')}")
    st.markdown("""
    This network graph highlights the interactions between genes, with edge types and interaction strengths clearly marked.
    """)

    image_path = f"images/{display_name}_legend.png"
    if os.path.exists(image_path):
        #st.image(image_path, caption=f"Explanation for {display_name}")
        # --- Layout with two columns ---
        #col1, col2 = st.columns([3, 3])  

        with st.container():
            st.markdown("<div style='display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            st.image(image_path, width=350)
            st.markdown("</div>", unsafe_allow_html=True)

        styled_html = f"""
            <style>
                .border-box {{
                    border: 2px solid #cccccc;
                    padding: 5px;
                    border-radius: 5px;
                }}
            </style>
            <div class="border-box">
                {open(f"images/{display_name}.html", "r").read()}
            </div>
            """
        with st.container():
            st.markdown("<div style='display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            st.components.v1.html(styled_html, height=500, scrolling=True)
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


