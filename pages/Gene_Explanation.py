import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import pandas as pd
from PIL import Image, ImageOps
import io

# --- Page setup ---
st.set_page_config(
    page_title="Gene Explanation",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
[data-testid="stSidebar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stApp { background-color: #f7f8fa; }
html, body, [class*="css"] { font-family: "IBM Plex Sans", sans-serif; }
.block-container {
    max-width: 960px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}
/* Back link */
.back-link a {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.75rem;
    color: #6b7a8d;
    text-decoration: none;
    letter-spacing: 0.05em;
}
.back-link a:hover { color: #2563eb; }
/* Gene header */
.gene-eyebrow {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.7rem; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #6b7a8d; margin-bottom: 0.4rem;
}
.gene-title {
    font-size: 2rem; font-weight: 600; color: #111827;
    letter-spacing: -0.02em; line-height: 1.2; margin-bottom: 0.5rem;
}
.gene-type-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.72rem; font-weight: 500;
    padding: 3px 12px; border-radius: 100px;
    margin-bottom: 1.5rem; letter-spacing: 0.03em;
}
.gene-type-badge.both { background: #e8f0fe; color: #1e40af; }
.gene-type-badge.ad   { background: #fef3c7; color: #92400e; }
.gene-type-badge.ar   { background: #f0fdf4; color: #166534; }
/* Summary card */
.summary-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    font-size: 0.925rem;
    color: #374151;
    line-height: 1.75;
}
.summary-card-label {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.65rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9ca3af; margin-bottom: 0.6rem;
}
/* Section headers */
.section-header {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9ca3af; margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e5e7eb;
}
/* Network wrapper */
.network-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
}
/* Dataframe overrides */
.stDataFrame { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrameResizable"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --- Query params ---
query_params = st.query_params
gene_name = query_params.get("gene", None)
gene_type = query_params.get("type", "both")

TAB_LABELS = {"both": "Autosomal Dominant + Recessive", "ad": "Autosomal Dominant Only", "ar": "Autosomal Recessive Only"}

if gene_type == "both":
    main_dir = "08012026_ad_ar/exps_short/"
elif gene_type == "ad":
    main_dir = "ad/exps_short/"
elif gene_type == "ar":
    main_dir = "ar/exps_short/"
else:
    main_dir = "08012026_ad_ar/exps_short/"
    gene_type = "both"

# --- No gene specified ---
if not gene_name:
    st.markdown("""
    <div style="text-align:center; padding: 4rem 1rem; color: #9ca3af;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🧬</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.85rem;">No gene specified in the URL.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

display_name = gene_name

# --- Back link ---
st.markdown(
    '<div class="back-link"><a href="/">← Back to predictions</a></div>',
    unsafe_allow_html=True
)

# --- Gene header ---
tab_label = TAB_LABELS.get(gene_type, "AD + AR")
st.markdown(f"""
<div class="gene-eyebrow">Gene Explanation</div>
<div class="gene-title">{display_name.replace("_", " ")}</div>
<span class="gene-type-badge {gene_type}">&#9654; {tab_label} model</span>
""", unsafe_allow_html=True)

# --- Summary ---
try:
    with open(main_dir + f"dee_summary_{display_name}_v2.txt", "r") as f:
        description_text = f.read()
except FileNotFoundError:
    description_text = "This gene has no connections to other genes in the data used for the predictive model."

st.markdown(f"""
<div class="summary-card">
    <div class="summary-card-label">Summary</div>
    {description_text}
</div>
""", unsafe_allow_html=True)

# --- Network visualisation ---
image_path = main_dir + f"{display_name}_legend_v2.png"
html_path  = main_dir + f"{display_name}_v2.html"

if os.path.exists(image_path) and os.path.exists(html_path):

    st.markdown('<div class="section-header">Gene Interaction Network</div>', unsafe_allow_html=True)

    # Encode legend
    with open(image_path, "rb") as img_file:
        legend_base64 = base64.b64encode(img_file.read()).decode()

    # Read and patch network HTML
    with open(html_path, "r") as f:
        html_content = f.read()

    html_content = html_content.replace(
        "<head>",
        """<head><style>
            body, html { margin: 0 !important; padding: 0 !important; overflow: hidden !important; background: #fff; }
            svg { display: block; margin: 0 auto; }
        </style>
        <script type="text/javascript">
            document.addEventListener("DOMContentLoaded", function() {
                if (window.network) {
                    const MIN_ZOOM = 0.5, MAX_ZOOM = 10;
                    network.on("zoom", function(params) {
                        if (params.scale < MIN_ZOOM) network.moveTo({ scale: MIN_ZOOM });
                        else if (params.scale > MAX_ZOOM) network.moveTo({ scale: MAX_ZOOM });
                    });
                }
            });
        </script>"""
    )

    # Trim legend whitespace and show as compact image
    legend_img = Image.open(image_path).convert("RGBA")
    bg = Image.new("RGBA", legend_img.size, (255, 255, 255, 255))
    diff = ImageOps.invert(Image.alpha_composite(bg, legend_img).convert("RGB"))
    bbox = diff.getbbox()
    if bbox:
        pad = 18
        bbox = (
            max(0, bbox[0] - pad), max(0, bbox[1] - pad),
            min(legend_img.width, bbox[2] + pad), min(legend_img.height, bbox[3] + pad)
        )
        legend_img = legend_img.crop(bbox)
    buf = io.BytesIO()
    legend_img.save(buf, format="PNG")
    buf.seek(0)

    legend_b64 = base64.b64encode(buf.getvalue()).decode()
    components.html(f"""
    <div style="
        background:#fff; border:1px solid #e5e7eb; border-radius:12px;
        padding:1rem 1.25rem 0.75rem; margin-bottom:1rem;
        box-shadow:0 1px 4px rgba(0,0,0,0.05); display:inline-block;
    ">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.63rem; font-weight:600;
            text-transform:uppercase; letter-spacing:0.1em; color:#9ca3af; margin-bottom:0.5rem;">
            Legend
        </div>
        <img src="data:image/png;base64,{legend_b64}"
             style="display:block; max-width:420px; width:100%; height:auto;" alt="Legend">
    </div>
    """, height=420)

    # Network
    network_html = f"""
    <!DOCTYPE html><html><head>
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ margin: 0 !important; padding: 0 !important; overflow: hidden !important; background: #fff; }}
    svg {{ display: block; margin: 0 auto; }}
    </style>
    </head><body>
    {html_content}
    </body></html>
    """

    st.markdown('<div class="network-card">', unsafe_allow_html=True)
    components.html(network_html, height=1200, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Connections table ---
    csv_path = main_dir + f"tabular_{display_name}.csv"
    if os.path.exists(csv_path):
        st.markdown('<div class="section-header" style="margin-top:1.5rem;">Gene Connections</div>', unsafe_allow_html=True)
        df = pd.read_csv(csv_path)
        df = df.rename(columns={
            "Sender":        "Source Gene",
            "Sender Label":  "Known DEE Gene (Source)",
            "Receiver":      "Target Gene",
            "Receiver Label":"Known DEE Gene (Target)",
            "Importance":    "Connection Importance",
            "Edge Type":     "Connection Type",
            "Pathways":      "Pathway Type(s)"
        })
        st.data_editor(df, use_container_width=True, height=500, hide_index=True)

        st.download_button(
            label="⬇ Download as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"{display_name}_connections.csv",
            mime="text/csv",
        )

else:
    st.markdown("""
    <div style="background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:2rem; text-align:center; color:#9ca3af; margin-top:1rem;">
        <div style="font-size:1.5rem; margin-bottom:0.5rem;">🔍</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.82rem;">No network visualisation found for this gene.</div>
    </div>
    """, unsafe_allow_html=True)