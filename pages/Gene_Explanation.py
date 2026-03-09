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
.back-link a {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.75rem; color: #6b7a8d;
    text-decoration: none; letter-spacing: 0.05em;
}
.back-link a:hover { color: #2563eb; }
.gene-eyebrow {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.7rem; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #6b7a8d; margin-bottom: 0.4rem; margin-top: 0.75rem;
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
.summary-card {
    background: #fff; border: 1px solid #e5e7eb; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    font-size: 0.925rem; color: #374151; line-height: 1.75;
}
.summary-card-label {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.65rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9ca3af; margin-bottom: 0.6rem;
}
.section-header {
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #9ca3af; margin-bottom: 0.75rem;
    padding-bottom: 0.5rem; border-bottom: 1px solid #e5e7eb;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrameResizable"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --- Query params ---
query_params = st.query_params
gene_name = query_params.get("gene", None)
gene_type = query_params.get("type", "both")

TAB_LABELS = {
    "both": "Autosomal Dominant + Recessive",
    "ad":   "Autosomal Dominant Only",
    "ar":   "Autosomal Recessive Only"
}

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
st.markdown('<div class="back-link"><a href="/">← Back to predictions</a></div>', unsafe_allow_html=True)

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

    # Trim legend whitespace
    legend_img = Image.open(image_path).convert("RGBA")
    bg   = Image.new("RGBA", legend_img.size, (255, 255, 255, 255))
    diff = ImageOps.invert(Image.alpha_composite(bg, legend_img).convert("RGB"))
    bbox = diff.getbbox()
    if bbox:
        pad  = 18
        bbox = (
            max(0, bbox[0] - pad), max(0, bbox[1] - pad),
            min(legend_img.width, bbox[2] + pad), min(legend_img.height, bbox[3] + pad)
        )
        legend_img = legend_img.crop(bbox)
    buf = io.BytesIO()
    legend_img.save(buf, format="PNG")
    legend_b64 = base64.b64encode(buf.getvalue()).decode()

    # Read and patch network HTML
    with open(html_path, "r") as f:
        html_content = f.read()

    # Expose vis.js network instance as a global so we can call fit()
    html_content = html_content.replace(
        "var network = new vis.Network(",
        "var network = window.network = new vis.Network("
    )

    html_content = html_content.replace(
        "<head>",
        """<head><style>
            body, html { margin: 0 !important; padding: 0 !important; background: #fff; }
        </style>
        <script type="text/javascript">
            window.addEventListener("message", function(e) {
                if (!window.network) return;
                if (e.data === "fit") window.network.fit({ animation: { duration: 400, easingFunction: "easeInOutQuad" } });
                if (e.data === "reset") window.network.moveTo({ scale: 1, position: { x: 0, y: 0 }, animation: { duration: 400, easingFunction: "easeInOutQuad" } });
            });
            document.addEventListener("DOMContentLoaded", function() {
                // Poll until network is ready then attach zoom limits
                const poll = setInterval(function() {
                    if (window.network) {
                        clearInterval(poll);
                        // Auto-fit once layout is stable
                        window.network.once("stabilized", function() {
                            window.network.fit({ animation: { duration: 400, easingFunction: "easeInOutQuad" } });
                        });
                        const MIN_ZOOM = 0.5, MAX_ZOOM = 10;
                        window.network.on("zoom", function(params) {
                            if (params.scale < MIN_ZOOM) window.network.moveTo({ scale: MIN_ZOOM });
                            else if (params.scale > MAX_ZOOM) window.network.moveTo({ scale: MAX_ZOOM });
                        });
                    }
                }, 200);
            });
        </script>"""
    )

    # Escape for srcdoc embedding
    srcdoc = html_content.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#39;")

    network_html = f"""<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: "IBM Plex Sans", sans-serif; background: #f7f8fa; overflow: hidden; }}

.card {{
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 640px;
}}

/* Toolbar */
.toolbar {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.5rem 1rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    flex-shrink: 0;
}}
.toolbar-title {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.63rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em; color: #9ca3af;
}}
.toolbar-actions {{ display: flex; gap: 6px; }}
.btn {{
    font-family: "IBM Plex Sans", sans-serif;
    font-size: 0.78rem; font-weight: 500;
    color: #374151; background: #fff;
    border: 1px solid #d1d5db; border-radius: 7px;
    padding: 4px 12px; cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
}}
.btn:hover {{ background: #f3f4f6; border-color: #9ca3af; }}

/* Network area */
.network-area {{ position: relative; flex: 1; overflow: hidden; }}
.network-frame {{ width: 100%; height: 100%; border: none; display: block; }}

/* Legend overlay — collapsible, top-right */
.legend-overlay {{
    position: absolute; top: 12px; right: 12px;
    background: rgba(255,255,255,0.97);
    border: 1px solid #e5e7eb; border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    overflow: hidden; z-index: 100;
    max-width: 280px; min-width: 160px;
    transition: box-shadow 0.2s;
}}
.legend-header {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 6px 10px;
    background: #f9fafb; border-bottom: 1px solid #e5e7eb;
    cursor: pointer; user-select: none;
}}
.legend-header-label {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.6rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em; color: #6b7a8d;
}}
.legend-toggle {{ font-size: 0.6rem; color: #9ca3af; transition: transform 0.2s; }}
.legend-body {{ padding: 8px 10px; }}
.legend-body img {{ display: block; width: 100%; height: auto; }}
.legend-overlay.collapsed .legend-body {{ display: none; }}
.legend-overlay.collapsed .legend-toggle {{ transform: rotate(180deg); }}
</style>
</head>
<body>
<div class="card">

  <div class="toolbar">
    <span class="toolbar-title">Interactive Network &mdash; Pan &amp; zoom to explore</span>
    <div class="toolbar-actions">
      <button class="btn" onclick="fitNetwork()">&#8853; Fit to screen</button>
    </div>
  </div>

  <div class="network-area">
    <iframe id="netFrame" class="network-frame" srcdoc="{srcdoc}"></iframe>

    <div class="legend-overlay" id="legendOverlay">
      <div class="legend-header" onclick="toggleLegend()">
        <span class="legend-header-label">Legend</span>
        <span class="legend-toggle" id="legendToggle">&#9650;</span>
      </div>
      <div class="legend-body">
        <img src="data:image/png;base64,{legend_b64}" alt="Legend">
      </div>
    </div>
  </div>

</div>

<script>
function fitNetwork() {{
  document.getElementById("netFrame").contentWindow.postMessage("fit", "*");
}}

function toggleLegend() {{
  document.getElementById("legendOverlay").classList.toggle("collapsed");
}}
</script>
</body>
</html>"""

    components.html(network_html, height=700, scrolling=False)

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