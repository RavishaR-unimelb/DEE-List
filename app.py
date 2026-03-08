import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# --- Page setup (must be first) ---
st.set_page_config(
    page_title="DEE Gene Predictions",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject only Streamlit-level overrides via markdown (sidebar hide, bg, container width)
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stApp { background-color: #f7f8fa; }
.block-container {
    max-width: 900px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}
.stTextInput > div > div > input {
    font-family: "IBM Plex Sans", sans-serif !important;
    font-size: 0.9rem !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    background: #ffffff !important;
    color: #111827 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
.stTextInput label, .stSelectbox label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Load JSON data ---
with open("predictions_A0.json", "r") as f:
    data = json.load(f)

# --- Prepare the DataFrame ---
df = pd.DataFrame(data["predictions"])
df = df.reset_index(drop=True)
df["Rank"] = df.index + 1
df = df[["Rank", "Gene", "Score"]]
df["Score"] = df["Score"].astype(float)

max_score = float(df["Score"].max())

HIGH_THRESHOLD   = 0.85
MEDIUM_THRESHOLD = 0.50

def get_confidence(score):
    if score >= HIGH_THRESHOLD:
        return "High"
    elif score >= MEDIUM_THRESHOLD:
        return "Medium"
    else:
        return "Low"

df["Confidence"] = df["Score"].apply(get_confidence)

n_high   = int((df["Confidence"] == "High").sum())
n_medium = int((df["Confidence"] == "Medium").sum())
n_low    = int((df["Confidence"] == "Low").sum())

# --- Filter function ---
def apply_filters():
    q    = st.session_state.get("search_query", "")
    conf = st.session_state.get("conf_filter", "All")
    filtered = df.copy()
    if q:
        filtered = filtered[filtered["Gene"].str.contains(q, case=False, na=False)]
    if conf != "All":
        filtered = filtered[filtered["Confidence"] == conf]
    st.session_state.display_df = filtered

# --- Session state ---
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "conf_filter" not in st.session_state:
    st.session_state.conf_filter = "All"

# Recompute display_df every run
_q    = st.session_state.get("search_query", "")
_conf = st.session_state.get("conf_filter", "All")
_filtered = df.copy()
if _q:
    _filtered = _filtered[_filtered["Gene"].str.contains(_q, case=False, na=False)]
if _conf != "All":
    _filtered = _filtered[_filtered["Confidence"] == _conf]
st.session_state.display_df = _filtered

# ── Header (via component) ───────────────────────────────────────────────────
components.html(f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: "IBM Plex Sans", sans-serif; background: transparent; padding: 0; }}
.eyebrow {{
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.7rem; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #6b7a8d; margin-bottom: 0.5rem;
}}
.title {{
    font-size: 2rem; font-weight: 600; color: #111827;
    letter-spacing: -0.02em; line-height: 1.2; margin-bottom: 0.75rem;
}}
.desc {{ font-size: 0.925rem; color: #4b5563; line-height: 1.7; max-width: 680px; margin-bottom: 1rem; }}
.desc a {{ color: #2563eb; text-decoration: none; font-weight: 500; }}
.meta-pill {{
    display: inline-flex; align-items: center; gap: 6px;
    background: #e8f0fe; color: #1e40af;
    font-family: "IBM Plex Mono", monospace;
    font-size: 0.72rem; font-weight: 500;
    padding: 4px 12px; border-radius: 100px;
    margin-bottom: 1rem; letter-spacing: 0.03em;
}}
.stats-strip {{ display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }}
.stat-card {{
    background: #fff; border: 1px solid #e5e7eb;
    border-radius: 10px; padding: 0.6rem 1.1rem; min-width: 100px;
}}
.stat-label {{
    font-family: "IBM Plex Mono", monospace; font-size: 0.63rem;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: #9ca3af; margin-bottom: 2px;
}}
.stat-value {{ font-size: 1.1rem; font-weight: 600; color: #111827; }}
.stat-value.high {{ color: #16a34a; }}
.stat-value.med  {{ color: #d97706; }}
.stat-value.low  {{ color: #dc2626; }}
.legend {{ display: flex; gap: 1.25rem; flex-wrap: wrap; align-items: center; }}
.legend-label {{
    font-family: "IBM Plex Mono", monospace; font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-right: 4px;
}}
.legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: #374151; }}
.legend-dot {{ width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }}
</style>
</head>
<body>
<div class="eyebrow">Genomics &middot; Predictive Model</div>
<div class="title">Top DEE Gene Predictions</div>
<div class="desc">
    Ranked predictions for Developmental &amp; Epileptic Encephalopathy genes based on the
    latest model outputs, trained on both AD and AR DEE genes.
    Also view: <a href="/only_ar_dee">Only AR DEE</a> &nbsp;&middot;&nbsp; <a href="/only_ad_dee">Only AD DEE</a>
</div>
<div class="meta-pill">&#10227; &nbsp;Last updated: {data["updated"]}</div>
<div class="stats-strip">
    <div class="stat-card"><div class="stat-label">Total Genes</div><div class="stat-value">{len(df)}</div></div>
    <div class="stat-card"><div class="stat-label">High Confidence</div><div class="stat-value high">{n_high}</div></div>
    <div class="stat-card"><div class="stat-label">Medium Confidence</div><div class="stat-value med">{n_medium}</div></div>
    <div class="stat-card"><div class="stat-label">Low Confidence</div><div class="stat-value low">{n_low}</div></div>
    <div class="stat-card"><div class="stat-label">Top Score</div><div class="stat-value">{max_score:.4f}</div></div>
</div>
<div class="legend">
    <span class="legend-label">Key:</span>
    <div class="legend-item"><div class="legend-dot" style="background:#16a34a"></div> High &ge; 0.85</div>
    <div class="legend-item"><div class="legend-dot" style="background:#d97706"></div> Medium 0.50 &ndash; 0.84</div>
    <div class="legend-item"><div class="legend-dot" style="background:#dc2626"></div> Low &lt; 0.50</div>
</div>
</body>
</html>
""", height=320)

# ── Search + filter (native Streamlit widgets) ───────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.text_input("Search genes", key="search_query", on_change=apply_filters, placeholder="e.g. SCN1A")
with col2:
    st.selectbox("Confidence", ["All", "High", "Medium", "Low"], key="conf_filter", on_change=apply_filters)

display_df = st.session_state.display_df
n     = len(display_df)
total = len(df)

# ── Table (via component so CSS is guaranteed to render) ─────────────────────
CONF_META = {
    "High":   ("high", "#16a34a"),
    "Medium": ("med",  "#d97706"),
    "Low":    ("low",  "#dc2626"),
}

def build_table_html(display_df, max_score, n, total):
    rows = ""
    for _, row in display_df.iterrows():
        rank  = int(row["Rank"])
        gene  = str(row["Gene"])
        score = float(row["Score"])
        conf  = str(row["Confidence"])

        url_safe    = gene.replace(" ", "_")
        pct         = int((score / max_score) * 100) if max_score > 0.0 else 0
        cls, color  = CONF_META.get(conf, ("low", "#dc2626"))
        badge_class = "rank-badge top3" if rank <= 3 else "rank-badge"

        rows += f"""
        <tr>
            <td><span class="{badge_class}">{rank}</span></td>
            <td><a href="/Gene_Explanation?gene={url_safe}" target="_top">{gene}</a></td>
            <td>
                <div class="score-cell">
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{pct}%;background:{color}"></div>
                    </div>
                    <span class="score-val {cls}">{score:.4f}</span>
                </div>
            </td>
            <td><span class="conf-badge {cls}">{conf}</span></td>
        </tr>"""

    if not rows:
        rows = '<tr><td colspan="4"><div class="no-results">No genes match your search.</div></td></tr>'

    return f"""<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: "IBM Plex Sans", sans-serif; background: transparent; }}
.result-count {{
    font-family: "IBM Plex Mono", monospace; font-size: 0.75rem;
    color: #9ca3af; margin-bottom: 1rem;
}}
.gene-table-wrapper {{
    background: #ffffff; border-radius: 12px;
    border: 1px solid #e5e7eb; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}}
table {{ width: 100%; border-collapse: collapse; font-size: 0.865rem; }}
thead tr {{ background: #f9fafb; border-bottom: 1.5px solid #e5e7eb; }}
thead th {{
    font-family: "IBM Plex Mono", monospace; font-size: 0.67rem;
    font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
    color: #6b7a8d; padding: 0.7rem 1rem; text-align: left; white-space: nowrap;
}}
tbody tr {{ border-bottom: 1px solid #f3f4f6; transition: background 0.12s ease; }}
tbody tr:last-child {{ border-bottom: none; }}
tbody tr:hover {{ background: #f8faff; }}
tbody td {{ padding: 0.65rem 1rem; color: #1f2937; vertical-align: middle; }}
.rank-badge {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px; border-radius: 50%;
    font-family: "IBM Plex Mono", monospace; font-size: 0.7rem; font-weight: 600;
    background: #f3f4f6; color: #6b7280;
}}
.rank-badge.top3 {{ background: #dbeafe; color: #1d4ed8; }}
a {{ color: #1d4ed8; font-weight: 500; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.score-cell {{ display: flex; align-items: center; gap: 8px; }}
.score-bar-bg {{
    width: 56px; height: 5px; background: #e5e7eb;
    border-radius: 99px; overflow: hidden; flex-shrink: 0;
}}
.score-bar-fill {{ height: 100%; border-radius: 99px; }}
.score-val {{ font-family: "IBM Plex Mono", monospace; font-size: 0.82rem; font-weight: 500; }}
.score-val.high {{ color: #15803d; }}
.score-val.med  {{ color: #b45309; }}
.score-val.low  {{ color: #b91c1c; }}
.conf-badge {{
    display: inline-flex; align-items: center;
    padding: 2px 10px; border-radius: 100px;
    font-size: 0.73rem; font-weight: 600; white-space: nowrap;
}}
.conf-badge.high {{ background: #dcfce7; color: #15803d; }}
.conf-badge.med  {{ background: #fef9c3; color: #a16207; }}
.conf-badge.low  {{ background: #fee2e2; color: #b91c1c; }}
.no-results {{ text-align: center; padding: 3rem 1rem; color: #9ca3af; font-size: 0.9rem; }}
</style>
</head>
<body>
<div class="result-count">Showing {n} of {total} genes</div>
<div class="gene-table-wrapper">
    <table>
        <thead>
            <tr>
                <th>Rank</th><th>Gene</th><th>Score</th><th>Confidence</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
</div>
</body>
</html>"""

table_html = build_table_html(display_df, max_score, n, total)
# Each row ~46px, thead ~44px, result-count ~28px, wrapper padding ~20px
row_count = max(len(display_df), 1)
height = 44 + 28 + row_count * 46 + 40
components.html(table_html, height=height, scrolling=False)