import streamlit as st
from urllib.parse import parse_qs
import os
import base64

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
    This network visualization illustrates the local interaction landscape of the gene. 
    Each node represents a gene, with color indicating its annotation (e.g., DEE or Unknown). 
    Edges denote biological interactions, with distinct colors for edge types (type1, type2, type3), 
    and numerical labels indicating the strength or importance of each connection. 
    This graph provides insight into the most influential genes and interactions contributing to the gene's classification.
    """)

    image_path = f"images/{display_name}_legend.png"
    if os.path.exists(image_path):
        #st.image(image_path, caption=f"Explanation for {display_name}")
        # --- Layout with two columns ---
        #col1, col2 = st.columns([3, 3])  



        # Step 1: Encode legend image as base64
        with open(image_path, "rb") as img_file:
            legend_base64 = base64.b64encode(img_file.read()).decode()

        # Step 2: Read HTML content and inject styles
        with open(f"images/{display_name}.html", "r") as f:
            html_content = f.read()

        # Optional: Ensure no extra margin/padding inside embedded HTML
        html_content = html_content.replace(
            "<head>",
            """<head><style>
                body, html {
                    margin: 0 !important;
                    padding: 0 !important;
                    overflow: hidden !important;
                }
                svg {
                    display: block;
                    margin: 0 auto;
                }
            </style>"""
        )

        # Step 3: Combine legend image and HTML in one styled container
        styled_html = f"""
            <style>
                .border-box {{
                    border: 2px solid #cccccc;
                    padding: 10px;
                    border-radius: 0px;
                    margin-top: 0px;
                    text-align: center;
                }}
                .legend-img {{
                    max-width: 400px;
                    margin-bottom: 2px;
                }}
            </style>
            <div class="border-box">
                <img class="legend-img" src="data:image/png;base64,{legend_base64}" alt="Legend">
                {html_content}
            </div>
        """

        # Step 4: Render everything
        st.components.v1.html(styled_html, height=1200, width=1200, scrolling=False)


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


