import streamlit as st
import pandas as pd
import json

# --- Function to filter dataframe based on search query ---
def filter_df():
    search_query = st.session_state.search_query
    if search_query == '':
        filtered_df = df
    else:
        filtered_df = df[df['Gene'].str.contains(search_query, case=False, na=False)]

    # Save the filtered dataframe to session state
    st.session_state.display_df = filtered_df

##################################

# --- Load JSON data ---
with open('prediction_output.json', 'r') as f:
    data = json.load(f)

# --- Prepare the DataFrame ---
df = pd.DataFrame(data['predictions'])
df = df.reset_index(drop=True)  # Reset old index
df['Rank'] = df.index + 1
df = df[['Rank', 'Gene', 'Score']]

def make_gene_link(gene_name):
    return f"[{gene_name}](/Gene_Explanation?gene={gene_name.replace(' ', '_')})"

df['Gene'] = df['Gene'].apply(make_gene_link)

# --- Page setup ---
st.set_page_config(page_title="Predictions Dashboard", layout="centered")

# --- Header ---
st.title("Top DEE Gene Predictions")

st.markdown(
    "This dashboard displays the top predicted DEE genes based on the "
    "latest model outputs. The displayed list of genes are obtained by training "
    "the model for both AD and AR DEE genes. For the ranked list obtained by "
    "using only AR DEE and only AD DEE genes: [Only AR DEE](/only_ar_dee), [Only AD DEE](/only_ad_dee)"
)

# --- Show last updated time ---
st.caption(f"**Last Updated:** {data['updated']}")

##################################

# --- Initialize session state ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''
if 'display_df' not in st.session_state:
    st.session_state.display_df = df

# --- Search bar with on_change callback ---
st.text_input("Search by gene:", key="search_query", on_change=filter_df)

# --- Display dataframe ---
st.dataframe(
    st.session_state.display_df.style
    .format({
        "Score": "{:.2f}"
    })
    .hide(axis="index")
)

st.markdown(
    st.session_state.display_df.to_html(escape=False, index=False),
    unsafe_allow_html=True
)
