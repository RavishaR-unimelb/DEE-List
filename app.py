import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# --- Page setup ---
st.set_page_config(
    page_title="DEE Gene Predictions",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
</style>
""", unsafe_allow_html=True)

# --- Load data ---
# ad + ar
with open("predictions_A0.json", "r") as f:
    data = json.load(f)

# only ad
with open("predictions_R_ad.json", "r") as f:
    data_ad = json.load(f)

# only ar
with open("predictions_R_ar.json", "r") as f:
    data_ar = json.load(f)

# ad + ar
df = pd.DataFrame(data["predictions"])
df = df.reset_index(drop=True)
df["Rank"] = df.index + 1
df = df[["Rank", "Gene", "Score"]]
df["Score"] = df["Score"].astype(float)

# only ad
df_ad = pd.DataFrame(data_ad["predictions"])
df_ad = df_ad.reset_index(drop=True)
df_ad["Rank"] = df_ad.index + 1
df_ad = df_ad[["Rank", "Gene", "Score"]]
df_ad["Score"] = df_ad["Score"].astype(float)

# only ar
df_ar = pd.DataFrame(data_ar["predictions"])
df_ar = df_ar.reset_index(drop=True)
df_ar["Rank"] = df_ar.index + 1
df_ar = df_ar[["Rank", "Gene", "Score"]]
df_ar["Score"] = df_ar["Score"].astype(float)

HIGH_THRESHOLD   = 0.85
MEDIUM_THRESHOLD = 0.50

def get_confidence(score):
    if score >= HIGH_THRESHOLD:   return "High"
    elif score >= MEDIUM_THRESHOLD: return "Medium"
    else:                           return "Low"

def prepare_genes(source_df, dee_type):
    d = source_df.copy()
    d["Score"]      = d["Score"].astype(float)
    d["Rank"]       = list(range(1, len(d) + 1))
    d["Confidence"] = d["Score"].apply(get_confidence)
    d["GeneLink"] = d["Gene"].apply(
        lambda g: f'<a href="/Gene_Explanation?gene={g.replace(" ", "_")}&type={dee_type}" target="_blank">{g}</a>'
    )
    return d[["Rank", "Gene", "GeneLink", "Score", "Confidence"]].to_json(orient="records")

# Swap these for separate files when ready
genes_both_json = prepare_genes(df, 'both')
genes_ad_json   = prepare_genes(df_ad, 'ad')
genes_ar_json   = prepare_genes(df_ar, 'ar')

updated = data["updated"]

HTML = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "IBM Plex Sans", sans-serif; background: transparent; padding-bottom: 8px; }

/* Header */
.eyebrow { font-family: "IBM Plex Mono", monospace; font-size: 0.7rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: #6b7a8d; margin-bottom: 0.5rem; }
.title { font-size: 2rem; font-weight: 600; color: #111827; letter-spacing: -0.02em; line-height: 1.2; margin-bottom: 0.75rem; }
.desc { font-size: 0.925rem; color: #4b5563; line-height: 1.7; max-width: 680px; margin-bottom: 1rem; }
.meta-pill { display: inline-flex; align-items: center; gap: 6px; background: #e8f0fe; color: #1e40af; font-family: "IBM Plex Mono", monospace; font-size: 0.72rem; font-weight: 500; padding: 4px 12px; border-radius: 100px; margin-bottom: 1.25rem; letter-spacing: 0.03em; }

/* Tabs */
.tab-bar { display: flex; gap: 4px; border-bottom: 2px solid #e5e7eb; margin-bottom: 1.25rem; }
.tab-btn { font-family: "IBM Plex Sans", sans-serif; font-size: 0.875rem; font-weight: 500; color: #6b7280; background: none; border: none; cursor: pointer; padding: 0.55rem 1.1rem; border-radius: 6px 6px 0 0; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: color 0.15s, border-color 0.15s; }
.tab-btn:hover { color: #2563eb; }
.tab-btn.active { color: #2563eb; border-bottom-color: #2563eb; font-weight: 600; }

/* Stats */
.stats-strip { display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; }
.stat-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 0.6rem 1.1rem; min-width: 100px; }
.stat-label { font-family: "IBM Plex Mono", monospace; font-size: 0.63rem; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-bottom: 2px; }
.stat-value { font-size: 1.1rem; font-weight: 600; color: #111827; }
.stat-value.high { color: #16a34a; } .stat-value.med { color: #d97706; } .stat-value.low { color: #dc2626; }

/* Legend */
.legend { display: flex; gap: 1.25rem; flex-wrap: wrap; align-items: center; margin-bottom: 1.25rem; }
.legend-label { font-family: "IBM Plex Mono", monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-right: 4px; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: #374151; }
.legend-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }

/* Controls */
.controls { display: flex; gap: 12px; margin-bottom: 8px; align-items: flex-end; }
.search-wrap { flex: 1; }
.search-wrap label, .select-wrap label { display: block; font-size: 0.8rem; font-weight: 500; color: #374151; margin-bottom: 4px; }
.search-wrap input { width: 100%; font-family: "IBM Plex Sans", sans-serif; font-size: 0.9rem; border: 1.5px solid #d1d5db; border-radius: 8px; padding: 0.55rem 1rem; background: #fff; color: #111827; outline: none; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: border-color 0.15s, box-shadow 0.15s; }
.search-wrap input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
.select-wrap select { font-family: "IBM Plex Sans", sans-serif; font-size: 0.875rem; border: 1.5px solid #d1d5db; border-radius: 8px; padding: 0.55rem 0.85rem; background: #fff; color: #111827; outline: none; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.result-count { font-family: "IBM Plex Mono", monospace; font-size: 0.75rem; color: #9ca3af; margin-bottom: 10px; }

/* Table */
.gene-table-wrapper { background: #fff; border-radius: 12px; border: 1px solid #e5e7eb; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
table { width: 100%; border-collapse: collapse; font-size: 0.865rem; }
thead tr { background: #f9fafb; border-bottom: 1.5px solid #e5e7eb; }
thead th { font-family: "IBM Plex Mono", monospace; font-size: 0.67rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #6b7a8d; padding: 0.7rem 1rem; text-align: left; white-space: nowrap; }
tbody tr { border-bottom: 1px solid #f3f4f6; transition: background 0.1s; }
tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: #f8faff; }
tbody td { padding: 0.65rem 1rem; color: #1f2937; vertical-align: middle; }
.rank-badge { display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 50%; font-family: "IBM Plex Mono", monospace; font-size: 0.7rem; font-weight: 600; background: #f3f4f6; color: #6b7280; }
.rank-badge.top3 { background: #dbeafe; color: #1d4ed8; }
a { color: #1d4ed8; font-weight: 500; text-decoration: none; }
a:hover { text-decoration: underline; }
.score-cell { display: flex; align-items: center; gap: 8px; }
.score-bar-bg { width: 56px; height: 5px; background: #e5e7eb; border-radius: 99px; overflow: hidden; flex-shrink: 0; }
.score-bar-fill { height: 100%; border-radius: 99px; }
.score-val { font-family: "IBM Plex Mono", monospace; font-size: 0.82rem; font-weight: 500; }
.score-val.high { color: #15803d; } .score-val.med { color: #b45309; } .score-val.low { color: #b91c1c; }
.conf-badge { display: inline-flex; align-items: center; padding: 2px 10px; border-radius: 100px; font-size: 0.73rem; font-weight: 600; white-space: nowrap; }
.conf-badge.high { background: #dcfce7; color: #15803d; }
.conf-badge.med  { background: #fef9c3; color: #a16207; }
.conf-badge.low  { background: #fee2e2; color: #b91c1c; }
.no-results { text-align: center; padding: 3rem 1rem; color: #9ca3af; font-size: 0.9rem; }
</style>
</head>
<body>

<div class="eyebrow">Gene Prioritization &middot; Predictive Model</div>
<div class="title">Developmental &amp; Epileptic Encephalopathy (DEE) Gene Predictions</div>
<div class="desc">Our model predicts candidate genes that may be linked to Developmental &amp; Epileptic Encephalopathy (DEE). These are genes not yet confirmed as DEE-associated, but which the model identifies as likely candidates based on their genomic and network features.</div>
<div class="meta-pill">&#10227; &nbsp;Last updated: __UPDATED__</div>

<div class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('both', this)">AD + AR</button>
  <button class="tab-btn" onclick="switchTab('ad', this)">Only AD</button>
  <button class="tab-btn" onclick="switchTab('ar', this)">Only AR</button>
</div>

<div class="stats-strip" id="statsStrip"></div>

<div class="legend">
  <span class="legend-label">Key:</span>
  <div class="legend-item"><div class="legend-dot" style="background:#16a34a"></div> High &ge; 0.85</div>
  <div class="legend-item"><div class="legend-dot" style="background:#d97706"></div> Medium 0.50 &ndash; 0.84</div>
  <div class="legend-item"><div class="legend-dot" style="background:#dc2626"></div> Low &lt; 0.50</div>
</div>

<div class="controls">
  <div class="search-wrap">
    <label for="geneSearch">Search genes</label>
    <input id="geneSearch" type="text" placeholder="e.g. SCN1A" oninput="filterTable()" autocomplete="off">
  </div>
  <div class="select-wrap">
    <label for="confSelect">Confidence</label>
    <select id="confSelect" onchange="filterTable()">
      <option value="All">All</option>
      <option value="High">High</option>
      <option value="Medium">Medium</option>
      <option value="Low">Low</option>
    </select>
  </div>
</div>

<div class="result-count" id="resultCount"></div>

<div class="gene-table-wrapper">
  <table>
    <thead><tr><th>Rank</th><th>Gene</th><th>Score</th><th>Confidence</th></tr></thead>
    <tbody id="tableBody"></tbody>
  </table>
</div>

<script>
const DATASETS = {
  both: __GENES_BOTH__,
  ad:   __GENES_AD__,
  ar:   __GENES_AR__,
};

let activeTab = "both";

const CONF_META = {
  High:   { cls: "high", color: "#16a34a" },
  Medium: { cls: "med",  color: "#d97706" },
  Low:    { cls: "low",  color: "#dc2626" },
};

function updateStats(genes) {
  const nHigh = genes.filter(g => g.Confidence === "High").length;
  const nMed  = genes.filter(g => g.Confidence === "Medium").length;
  const nLow  = genes.filter(g => g.Confidence === "Low").length;
  const top   = Math.max(...genes.map(g => g.Score)).toFixed(4);
  document.getElementById("statsStrip").innerHTML =
    `<div class="stat-card"><div class="stat-label">Total Genes</div><div class="stat-value">${genes.length}</div></div>` +
    `<div class="stat-card"><div class="stat-label">High Confidence</div><div class="stat-value high">${nHigh}</div></div>` +
    `<div class="stat-card"><div class="stat-label">Medium Confidence</div><div class="stat-value med">${nMed}</div></div>` +
    `<div class="stat-card"><div class="stat-label">Low Confidence</div><div class="stat-value low">${nLow}</div></div>` +
    `<div class="stat-card"><div class="stat-label">Top Score</div><div class="stat-value">${top}</div></div>`;
}

function buildRow(g, maxScore) {
  const meta     = CONF_META[g.Confidence] || CONF_META.Low;
  const pct      = Math.round((g.Score / maxScore) * 100);
  const badgeCls = g.Rank <= 3 ? "rank-badge top3" : "rank-badge";
  return `<tr>
    <td><span class="${badgeCls}">${g.Rank}</span></td>
    <td>${g.GeneLink}</td>
    <td><div class="score-cell"><div class="score-bar-bg"><div class="score-bar-fill" style="width:${pct}%;background:${meta.color}"></div></div><span class="score-val ${meta.cls}">${g.Score.toFixed(4)}</span></div></td>
    <td><span class="conf-badge ${meta.cls}">${g.Confidence}</span></td>
  </tr>`;
}

function switchTab(tab, btn) {
  activeTab = tab;
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById("geneSearch").value = "";
  document.getElementById("confSelect").value = "All";
  updateStats(DATASETS[tab]);
  filterTable();
}

function filterTable() {
  const q        = document.getElementById("geneSearch").value.trim().toLowerCase();
  const conf     = document.getElementById("confSelect").value;
  const genes    = DATASETS[activeTab];
  const maxScore = Math.max(...genes.map(g => g.Score));
  const filtered = genes.filter(g =>
    (q === "" || g.Gene.toLowerCase().includes(q)) &&
    (conf === "All" || g.Confidence === conf)
  );
  document.getElementById("tableBody").innerHTML = filtered.length === 0
    ? `<tr><td colspan="4"><div class="no-results">No genes match your search.</div></td></tr>`
    : filtered.map(g => buildRow(g, maxScore)).join("");
  document.getElementById("resultCount").textContent =
    `Showing ${filtered.length} of ${genes.length} genes`;
}

updateStats(DATASETS[activeTab]);
filterTable();
</script>
</body>
</html>
"""

html_out = (HTML
    .replace("__UPDATED__",    updated)
    .replace("__GENES_BOTH__", genes_both_json)
    .replace("__GENES_AD__",   genes_ad_json)
    .replace("__GENES_AR__",   genes_ar_json)
)

components.html(html_out, height=6000, scrolling=False)