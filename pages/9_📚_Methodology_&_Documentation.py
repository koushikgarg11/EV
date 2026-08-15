import os
import sys

# Ensure root directory and src directory are in sys.path for robust imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import streamlit as st

try:
    from src.components import render_key_insights, apply_custom_theme
except Exception:
    try:
        from components import render_key_insights, apply_custom_theme
    except Exception:
        def apply_custom_theme():
            pass
        def render_key_insights(title="💡 Key Insights", insights=None, badge_text="⚡ EXECUTIVE METRICS", **kwargs):
            if insights is None:
                insights = ["No key insights available."]
            items = "".join([f"<div style='color:#FFFFFF !important;'><b>{i}</b></div>" for i in insights])
            st.markdown(f"<div style='padding:16px;border:1px solid rgba(56,189,248,0.3);border-radius:12px;background:#0f1724;color:#FFFFFF !important;'>{items}</div>", unsafe_allow_html=True)

st.set_page_config(page_title="Methodology & Documentation", page_icon="📚", layout="wide")

# Apply theme with inline fallback
st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }
    p, span, label, li, h1, h2, h3, h4, h5, h6, td, th {
        color: #FFFFFF !important;
    }
    header[data-testid="stHeader"], [data-testid="stHeader"], .stAppHeader, .stHeader, div[data-testid="stToolbar"] {
        background-color: #0E1117 !important;
        background: #0E1117 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stDecoration"] {
        background-image: none !important;
        background-color: #0E1117 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        background: #000000 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="select"] input, .stSelectbox div[role="button"], .stMultiSelect div[role="button"], div[data-baseweb="base-input"] {
        background-color: #161B22 !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        color: #FFFFFF !important;
    }
    span[data-baseweb="tag"], div[data-baseweb="tag"] {
        background: linear-gradient(90deg, rgba(0, 230, 118, 0.25), rgba(56, 189, 248, 0.2)) !important;
        border: 1px solid #00E676 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }
    span[data-baseweb="tag"] *, div[data-baseweb="tag"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }
    ul[data-baseweb="menu"], div[data-baseweb="popover"], div[data-baseweb="popover"] * {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
    }
    li[data-baseweb="option"] {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
    }
    li[data-baseweb="option"]:hover {
        background-color: rgba(56, 189, 248, 0.25) !important;
        color: #FFFFFF !important;
    }
    .stPlotlyChart, div[data-testid="stPlotlyChart"] {
        background-color: #0E1117 !important;
        background: #0E1117 !important;
        border-radius: 14px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        padding: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

try:
    apply_custom_theme()
except Exception:
    pass

st.title("📚 Methodology & Project Documentation")
st.markdown("### *BRD, PRD, Data Catalogue, and System Architecture.*")
st.markdown("---")

DOCS_DIR = os.path.join(BASE_DIR, "docs")

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

st.markdown("---")

render_key_insights(
    title="💡 Key Insights & Technical Architecture Summary",
    insights=[
        "<b>Rigorous MCDA Foundation:</b> Mathematically sound AHP-TOPSIS multi-criteria optimization removes bias from multi-million dollar site selections.",
        "<b>Sub-Second Spatial Search:</b> SciPy KDTree spatial partitioning delivers <b>O(log N)</b> distance lookup complexity across 130,000+ points.",
        "<b>Production Modular Architecture:</b> Clean separation of DB engine, GIS processing, MCDA decision engine, and Streamlit UI layer."
    ],
    badge_text="⚡ ARCHITECTURE AUDIT"
)
