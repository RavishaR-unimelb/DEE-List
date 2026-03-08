import streamlit as st
import pandas as pd
import json

# --- Page setup (must be first) ---
st.set_page_config(
    page_title="DEE Gene Predictions",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* Global font */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Hide sidebar */
[data-testid="stSidebar"] { display: none; }

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Page background */
.stApp {
    background-color: #f7f8fa;
}

/* Main container */
.block-container {
    max-width: 780px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}

/* Header section */
.header-block {
    margin-bottom: 2rem;
}

.header-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7a8d;
    margin-bottom: 0.5rem;
}

.header-title {
    font-size: 2rem;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-bottom: 0.75rem;
}

.header-desc {
    font-size: 0.925rem;
    color: #4b5563;
    line-height: 1.7;
    max-width: 620px;
}

.header-desc a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
}

.header-desc a:hover {
    text-decoration: underline;
}

/* Meta pill */
.meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #e8f0fe;
    color: #1e40af;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 2rem;
    letter-spacing: 0.03em;
}

/* Search box override */
.stTextInput > div > div > input {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.9rem !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    background: #ffffff !important;
    color: #111827 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

.stTextInput label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 4px !important;
}

/* Result count */
.result-count {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.4rem;
    margin-bottom: 1rem;
}

/* Table styling */
.gene-table-wrapper {
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.gene-table-wrapper table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}

.gene-table-wrapper thead tr {
    background: #f9fafb;
    border-bottom: 1.5px solid #e5e7eb;
}

.gene-table-wrapper thead th {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7a8d;
    padding: 0.75rem 1.25rem;
    text-align: left;
}

.gene-table-wrapper thead th:first-child { width: 64px; }
.gene-table-wrapper thead th:last-child  { text-align: right; }

.gene-table-wrapper tbody tr {
    border-bottom: 1px solid #f3f4f6;
    transition: background 0.12s ease;
}

.gene-table-wrapper tbody tr:last-child { border-bottom: none; }
.gene-table-wrapper tbody tr:hover { background: #f0f4ff; }

.gene-table-wrapper tbody td {
    padding: 0.75rem 1.25rem;
    color: #1f2937;
    vertical-align: middle;
}

.gene-table-wrapper tbody td:last-child {
    text-align: right;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #374151;
}

/* Rank badge */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    background: #f3f4f6;
    color: #6b7280;
}

.rank-badge.top3 {
    background: #dbeafe;
    color: #1d4ed8;
}

/* Gene link */
.gene-table-wrapper a {
    color: #1d4ed8;
    font-weight: 500;
    text-decoration: none;
    font-size: 0.9rem;
}

.gene-table-wrapper a:hover {
    color: #1e40af;
    text-decoration: underline;
}

/* Score bar */
.score-cell {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
}

.score-bar-bg {
    width: 72px;
    height: 5px;
    background: #e5e7eb;
    border-radius: 99px;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    border-radius: 99px;
}

/* No results */
.no-results {
    text-align: center;
    padding: 3rem 1rem;
    color: #9ca3af;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)


# --- Load JSON data ---
with open('predictions_A0.json', 'r') as f:
    data = json.load(f)

# --- Prepare the DataFrame ---
df = pd.DataFrame(data['predictions'])
df = df.reset_index(drop=True)
df['Rank'] = df.index + 1
df = df[['Rank', 'Gene', 'Score']]

max_score = df['Score'].max()

# --- Filter function ---
def filter_df():
    q = st.session_state.search_query
    if q == '':
        st.session_state.display_df = df
    else:
        st.session_state.display_df = df[df['Gene'].str.contains(q, case=False, na=False)]

# --- Initialize session state ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''
if 'display_df' not in st.session_state:
    st.session_state.display_df = df

# --- Header ---
st.markdown("""
<div class="header-block">
    <div class="header-eyebrow">Genomics · Predictive Model</div>
    <div class="header-title">Top DEE Gene Predictions</div>
    <div class="header-desc">
        Ranked predictions for Developmental &amp; Epileptic Encephalopathy genes based on the latest model outputs,
        trained on both AD and AR DEE genes.
        Also view rankings using <a href="/only_ar_dee">Only AR DEE</a> or <a href="/only_ad_dee">Only AD DEE</a>.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="meta-pill">⟳ &nbsp;Last updated: {data["updated"]}</div>', unsafe_allow_html=True)

# --- Search ---
st.text_input("Search genes", key="search_query", on_change=filter_df, placeholder="e.g. SCN1A")

display_df = st.session_state.display_df
n = len(display_df)
total = len(df)
st.markdown(
    f'<div class="result-count">Showing {n} of {total} genes</div>',
    unsafe_allow_html=True
)

# --- Build HTML table ---
def build_table(display_df, max_score):
    rows = ""
    for _, row in display_df.iterrows():
        rank = int(row['Rank'])
        gene = row['Gene']
        score = float(row['Score'])
        url_safe = gene.replace(' ', '_')
        pct = int((score / max_score) * 100) if max_score > 0 else 0
        badge_class = "rank-badge top3" if rank <= 3 else "rank-badge"
        rows += f"""
        <tr>
            <td><span class="{badge_class}">{rank}</span></td>
            <td><a href="/Gene_Explanation?gene={url_safe}">{gene}</a></td>
            <td>
                <div class="score-cell">
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{pct}%"></div>
                    </div>
                    {score:.4f}
                </div>
            </td>
        </tr>"""

    if not rows:
        rows = '<tr><td colspan="3"><div class="no-results">No genes match your search.</div></td></tr>'

    return f"""
    <div class="gene-table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Gene</th>
                    <th style="text-align:right">Score</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """

st.markdown(build_table(display_df, max_score), unsafe_allow_html=True)