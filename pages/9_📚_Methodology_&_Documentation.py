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

    # Render a self-contained HTML document with MathJax to reliably display formulas
    cards_html = """
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start;">
      <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px;">
        <h4>1. Haversine Spatial Distance Formula</h4>
        <p>Calculates exact great-circle distance between POI coordinates \((lat_1, lon_1)\) and charger coordinates \((lat_2, lon_2)\):</p>
        <div class="formula">$$\n\text{d} = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)\n$$</div>
        <p style="font-size: 0.85rem; color: #8B949E;">Where \(r = 6371\text{ km}\), \(\phi\) is latitude in radians, and \(\lambda\) is longitude in radians.</p>
      </div>

      <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px;">
        <h4>3. TOPSIS Closeness Coefficient</h4>
        <p>Relative closeness to ideal solution \(S^+\) and negative ideal solution \(S^-\):</p>
        <div class="formula">$$\nC_i^* = \frac{d_i^-}{d_i^+ + d_i^-}, \quad C_i^* \in [0, 1]\n$$</div>
        <p style="font-size: 0.85rem; color: #8B949E;">Candidate site with \(C_i^*\) closest to 1.0 receives highest investment rank.</p>
      </div>

      <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px;">
        <h4>2. AHP Criterion Weighting (Analytic Hierarchy Process)</h4>
        <p>Pairwise comparison matrix \(A\) yields principal eigenvector \(w\) representing criterion weight importance:</p>
        <div class="formula">$$\nA w = \lambda_{\max} w, \quad \text{Consistency Ratio (CR)} = \frac{CI}{RI} < 0.10\n$$</div>
      </div>

      <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 20px;">
        <h4>4. Charging Desert Severity Index Formula</h4>
        <p>Quantifies unserved commercial demand severity:</p>
        <div class="formula">$$\n\text{Severity}_i = 0.60 \times \left(\frac{\text{Footfall}_i}{\text{Footfall}_{max}}\right) + 0.40 \times \left(\frac{\text{DistToCharger}_i}{50\text{ km}}\right)\n$$</div>
      </div>
    </div>
    """

    # Build html_doc without f-string to avoid accidental brace interpretation
    html_doc = """<!doctype html>
    <html lang=\"en\"> 
    <head>
      <meta charset=\"utf-8\">
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
      <style>
        body { background: transparent; color: #E6EEF3; font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial; margin:0; padding:12px }
        h4 { margin:0 0 8px 0; color:#E6EEF3 }
        p { color:#b9c1c8 }
        .formula { background: #0b1220; padding:14px; border-radius:8px; margin-top:8px; color:#e6f7ff }
      </style>
      <!-- MathJax 3 CDN -->
      <script>
      window.MathJax = {};
      </script>
      <script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>
    </head>
    <body>
    """

    html_doc = html_doc + cards_html + """
    </body>
    </html>
    """

    import base64
    try:
        b64 = base64.b64encode(html_doc.encode('utf-8')).decode('ascii')
        data_uri = "data:text/html;charset=utf-8;base64," + b64
        st.iframe(data_uri, height=680)
    except Exception:
        st.markdown(cards_html, unsafe_allow_html=True)

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

