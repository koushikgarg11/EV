import os
import sys

# Ensure root directory is in sys.path for robust imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.components import render_key_insights

st.set_page_config(page_title="Methodology & Documentation", page_icon="📚", layout="wide")

st.title("📚 Methodology, Mathematical Logic & Project Documentation")
st.markdown("### *Mathematical formulations, spatial GIS algorithms, BRD, PRD, Data Catalogue, and Architecture.*")
st.markdown("---")

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

# Tabbed Documentation Interface
tab_math, tab_docs = st.tabs(["🧮 Mathematical Formulations & GIS Algorithms", "📄 Project Documentation (BRD/PRD/Architecture)"])

with tab_math:
    st.subheader("🧮 Decision Intelligence Mathematical Core")

    # Use Streamlit native rendering for math to avoid iframe parsing issues
    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown("""
            <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h4>1. Haversine Spatial Distance Formula</h4>
                <p>Calculates exact great-circle distance between POI coordinates (lat_1, lon_1) and charger coordinates (lat_2, lon_2):</p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(r"\text{d} = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)")
            st.markdown("""<p style='font-size:0.85rem;color:#8B949E'>Where r = 6371 km, \(\phi\) is latitude in radians, and \(\lambda\) is longitude in radians.</p>""", unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px;">
                <h4>2. AHP Criterion Weighting (Analytic Hierarchy Process)</h4>
                <p>Pairwise comparison matrix A yields principal eigenvector w representing criterion weight importance:</p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(r"A w = \lambda_{\max} w")
            st.markdown("""<p style='font-size:0.85rem;color:#8B949E'>Consistency Ratio (CR) = CI / RI &lt; 0.10</p>""", unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown("""
            <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h4>3. TOPSIS Closeness Coefficient</h4>
                <p>Relative closeness to ideal solution S<sup>+</sup> and negative ideal solution S<sup>-</sup>:</p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(r"C_i^* = \frac{d_i^-}{d_i^+ + d_i^-}")
            st.markdown("""<p style='font-size:0.85rem;color:#8B949E'>Candidate site with C_i^* closest to 1.0 receives highest investment rank.</p>""", unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px;">
                <h4>4. Charging Desert Severity Index Formula</h4>
                <p>Quantifies unserved commercial demand severity:</p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(r"\text{Severity}_i = 0.60 \times \left(\frac{\text{Footfall}_i}{\text{Footfall}_{max}}\right) + 0.40 \times \left(\frac{\text{DistToCharger}_i}{50\text{\ km}}\right)")

with tab_docs:
    st.sidebar.header("🎯 Documentation Navigation")
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

