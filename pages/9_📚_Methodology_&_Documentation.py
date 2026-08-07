import os
import streamlit as st

st.set_page_config(page_title="Methodology & Documentation", page_icon="📚", layout="wide")

st.title("📚 Methodology & Project Documentation")
st.markdown("### *Technical architecture, BRD, PRD, Data Catalogue, and GIS formulas.*")
st.markdown("---")

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

doc_option = st.sidebar.radio(
    "Select Document to View",
    ["BRD (Business Requirement Document)", "PRD (Product Requirement Document)", "Data Catalogue", "System Architecture"]
)

doc_map = {
    "BRD (Business Requirement Document)": "BRD.md",
    "PRD (Product Requirement Document)": "PRD.md",
    "Data Catalogue": "DATA_CATALOGUE.md",
    "System Architecture": "ARCHITECTURE.md"
}

target_file = os.path.join(DOCS_DIR, doc_map[doc_option])

if os.path.exists(target_file):
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
    st.markdown(content)
else:
    st.error(f"Document {doc_map[doc_option]} not found at {target_file}")
