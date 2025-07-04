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

        

        styled_html = f"""
            <style>
                .border-box {{
                    border: 2px solid #cccccc;
                    padding: 10px;
                    border-radius: 10px;
                    margin-top: 0px;
                }}
            </style>
            <div class="border-box">
                {open(f"images/{display_name}.html", "r").read()}
            </div>
            """
       
        with st.container():
            st.markdown("<div style='display: flex; align-items: left; justify-content: left;'>", unsafe_allow_html=True)
            st.image(image_path, width=400)

            #st.markdown("<div style='display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            st.components.v1.html(styled_html, height=1200, width=1200, scrolling=False)
            st.markdown("</div>", unsafe_allow_html=True)
            
        

        #with st.container():
            #st.markdown("<div style='display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
            #st.image(image_path, width=500)


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


