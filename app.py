import os
import sys
import streamlit as st
import pandas as pd

# Add src to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database.db_manager import db
from src.config import DEFAULT_MCDA_WEIGHTS

st.set_page_config(
    page_title="India EV Charging Gap Analysis Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Mode Glassmorphic Styling
st.markdown("""
<style>
    /* Dark Theme Customization */
    .stApp {
        background-color: #0E1117;
        color: #E0E6ED;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="metric-container"] label {
        color: #8B949E !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #00E676 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Section Cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00C853, #00E676);
        color: #000000;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load cached 1.3L datasets
@st.cache_data(ttl=3600)
def load_datasets():
    df_chargers = db.load_raw_dataset("ev_charging_stations")
    df_vahan = db.load_raw_dataset("vahan_ev_registrations")
    df_pois = db.load_raw_dataset("points_of_interest")
    df_power = db.load_raw_dataset("power_substations")
    df_highways = db.load_raw_dataset("highway_corridors")
    return df_chargers, df_vahan, df_pois, df_power, df_highways

try:
    df_chargers, df_vahan, df_pois, df_power, df_highways = load_datasets()
    total_records = len(df_chargers) + len(df_vahan) + len(df_pois) + len(df_power) + len(df_highways)
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# Header Banner
st.title("⚡ India EV Charging Infrastructure Gap Analysis & Site Recommendation Platform")
st.markdown("### *Data-driven spatial decision intelligence for expanding India's EV charging network efficiently.*")

st.markdown("---")

# Global KPIs
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Datasets Loaded", f"{total_records:,}", delta="1.3 Lakh Scale")
with col2:
    st.metric("EV Charging Stations", f"{len(df_chargers):,}", delta="OSM + OpenChargeMap")
with col3:
    st.metric("Vahan EV Records", f"{len(df_vahan):,}", delta="District & RTO Level")
with col4:
    st.metric("Commercial POIs", f"{len(df_pois):,}", delta="Demand Drivers")
with col5:
    st.metric("Highway Segments", f"{len(df_highways):,}", delta="NH-48, NH-44, NH-65+")

st.markdown("---")

st.markdown("""
<div class="glass-card">
    <h2>🚀 Welcome to the Decision Intelligence Platform</h2>
    <p>This platform integrates publicly available geospatial and transportation datasets across India to identify <b>charging deserts</b>, evaluate <b>highway corridor readiness</b>, and provide <b>explainable recommendations</b> for infrastructure investments.</p>
    <ul>
        <li><b>📌 Executive Summary</b>: Overview of India's EV ecosystem & adoption trends.</li>
        <li><b>🗺️ Spatial Infrastructure</b>: PyDeck 3D Hexagon density layers & interactive Folium map.</li>
        <li><b>📊 Demand Analytics</b>: Vahan EV registrations, 2W/3W/4W growth rates by district.</li>
        <li><b>🌵 Charging Desert Analysis</b>: Automated detection of underserved high-demand zones.</li>
        <li><b>🛣️ Highway Corridor Readiness</b>: Gap analysis along major National Highways.</li>
        <li><b>🎯 Site Recommendation Engine</b>: MCDA AHP/TOPSIS ranker with explainable score breakdowns.</li>
        <li><b>🎛️ Scenario Simulator</b>: What-if slider analysis for weight customization.</li>
        <li><b>📈 Data Quality Monitor</b>: Live dataset freshness, missingness, and coordinate validity checks.</li>
        <li><b>📚 Methodology & PRD</b>: Technical specs, math formulas, and system documentation.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation Note
st.sidebar.image("https://img.icons8.com/color/96/000000/electric-vehicle.png", width=80)
st.sidebar.title("Navigation Menu")
st.sidebar.info("Select a page from the menu above to explore specific modules.")
st.sidebar.markdown("---")
st.sidebar.caption("⚡ Powered by SciPy KDTree, GeoPandas & PyDeck")
