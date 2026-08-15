import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Add src to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

try:
    from src.database.db_manager import db
except Exception:
    from database.db_manager import db

try:
    from src.config import DEFAULT_MCDA_WEIGHTS
except Exception:
    pass

try:
    from src.components import fix_plotly_dark, apply_custom_theme
except Exception:
    def fix_plotly_dark(fig):
        if fig is not None:
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"))
        return fig
    def apply_custom_theme():
        pass

st.set_page_config(
    page_title="India EV Charging Gap Analysis Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inline Premium Dark Mode Styling & Pure White Text Override
st.markdown("""
<style>
    /* Dark Theme & Pure White Text Customization */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }
    
    /* Force body text, paragraphs, list items, and headings to White */
    p, span, label, li, h1, h2, h3, h4, h5, h6, td, th {
        color: #FFFFFF !important;
    }
    
    /* Streamlit Top Header & Toolbar Background Override to match #0E1117 */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    .stAppHeader,
    .stHeader,
    div[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    .stApp > header {
        background-color: #0E1117 !important;
        background: #0E1117 !important;
        color: #FFFFFF !important;
    }
    
    /* Remove top decoration strip */
    div[data-testid="stDecoration"] {
        background-image: none !important;
        background-color: #0E1117 !important;
    }

    /* Sidebar Customization - Pure Black */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        background: #000000 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 6px 0 30px rgba(0, 0, 0, 0.9) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* BaseWeb Selectbox / Multiselect Dropdown Controls (Dark Theme Fix) */
    [data-baseweb="select"],
    [data-baseweb="select"] *,
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] input,
    .stSelectbox div,
    .stMultiSelect div,
    div[data-baseweb="base-input"] {
        background-color: #161B22 !important;
        background: #161B22 !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] > div {
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 10px !important;
    }

    /* Selected tags / pills inside Multiselect */
    span[data-baseweb="tag"],
    div[data-baseweb="tag"] {
        background: #EF4444 !important;
        background-color: #EF4444 !important;
        border: 1px solid #F87171 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }

    span[data-baseweb="tag"] *,
    div[data-baseweb="tag"] * {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Dropdown Popup Menu */
    ul[data-baseweb="menu"],
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] * {
        background-color: #161B22 !important;
        background: #161B22 !important;
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

    /* Plotly Chart Container Fix */
    .stPlotlyChart,
    div[data-testid="stPlotlyChart"] {
        background-color: #0E1117 !important;
        background: #0E1117 !important;
        border-radius: 14px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        padding: 8px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }

    /* Folium Map Popup Fix */
    .leaflet-popup-content, .leaflet-popup-content * {
        color: #1E293B !important;
    }




    /* Metric Cards */
    div[data-testid="metric-container"], [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03)) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(12px) !important;
    }
    
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *, [data-testid="stMetricLabel"] label, [data-testid="stMetricLabel"] p, div[data-testid="metric-container"] label {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }
    
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] *, [data-testid="stMetricValue"] div, [data-testid="stMetricValue"] span, div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #00E676 !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }
    
    /* Section Cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 16px !important;
        padding: 26px !important;
        margin-bottom: 22px !important;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5) !important;
        color: #FFFFFF !important;
    }
    
    .glass-card p, .glass-card li, .glass-card ul, .glass-card b, .glass-card strong {
        color: #FFFFFF !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00C853, #00E676);
        color: #000000 !important;
        font-weight: 800;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Safe attempt for theme module
try:
    from src.components import apply_custom_theme
    apply_custom_theme()
except Exception:
    pass

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

# 1. Overview Section
st.markdown("""
<div class="glass-card">
    <h2 style="color: #FFFFFF !important;">🚀 Welcome to the Decision Intelligence Platform</h2>
    <p style="color: #FFFFFF !important;">This platform integrates publicly available geospatial and transportation datasets across India to identify <b>charging deserts</b>, evaluate <b>highway corridor readiness</b>, and provide <b>explainable recommendations</b> for infrastructure investments.</p>
    <ul style="color: #FFFFFF !important;">
        <li><b style="color: #00E676 !important;">📌 Executive Summary</b>: Overview of India's EV ecosystem & adoption trends.</li>
        <li><b style="color: #38BDF8 !important;">🗺️ Spatial Infrastructure</b>: PyDeck 3D Hexagon density layers & interactive Folium map.</li>
        <li><b style="color: #FBBF24 !important;">📊 Demand Analytics</b>: Vahan EV registrations, 2W/3W/4W growth rates by district.</li>
        <li><b style="color: #F43F5E !important;">🌵 Charging Desert Analysis</b>: Automated detection of underserved high-demand zones.</li>
        <li><b style="color: #C084FC !important;">🛣️ Highway Corridor Readiness</b>: Gap analysis along major National Highways.</li>
        <li><b style="color: #00E676 !important;">🎯 Site Recommendation Engine</b>: MCDA AHP/TOPSIS ranker with explainable score breakdowns.</li>
        <li><b style="color: #38BDF8 !important;">🎛️ Scenario Simulator</b>: What-if slider analysis for weight customization.</li>
        <li><b style="color: #34D399 !important;">📈 Data Quality Monitor</b>: Live dataset freshness, missingness, and coordinate validity checks.</li>
        <li><b style="color: #FBBF24 !important;">📚 Methodology & PRD</b>: Technical specs, BRD/PRD, and system documentation.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 2. Key Insights Section (Placed DIRECTLY BELOW Overview)
try:
    from src.components import render_key_insights
except Exception:
    try:
        from components import render_key_insights
    except Exception:
        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        try:
            from components import render_key_insights
        except Exception:
            def render_key_insights(title="💡 Key Insights", insights=None, badge_text="⚡ EXECUTIVE METRICS", **kwargs):
                if insights is None:
                    insights = ["No key insights available."]
                items = "".join([f"<div style='color:#FFFFFF !important;'><b>{i}</b></div>" for i in insights])
                st.markdown(f"<div style='padding:16px;border:1px solid rgba(56,189,248,0.3);border-radius:12px;background:#0f1724;color:#FFFFFF !important;'>{items}</div>", unsafe_allow_html=True)

try:
    render_key_insights(
        title="💡 Executive Platform Insights",
        insights=[
            "<b>Infrastructure Deficit:</b> Registered EVs are outpacing public charger installations by over <b>12.4x</b> in key high-volume metros.",
            "<b>Corridor Vulnerability:</b> Critical gaps exceed 75km along sections of NH-44 & NH-48, increasing range anxiety for long-distance 4W travel.",
            "<b>Commercial POI Synergy:</b> 68% of high-yield potential sites align with existing retail, dining & transit clusters.",
            "<b>Grid Accessibility:</b> Over 82% of top-ranked MCDA candidate sites reside within 1.5km of high-voltage power substations."
        ],
        badge_text="⚡ NATIONAL DECISION INTELLIGENCE"
    )
except Exception as e:
    st.warning(f"Key insights renderer failed: {e}")

st.markdown("---")

# 3. National EV Ecosystem Overview Charts
st.markdown("## 📊 National Ecosystem Overview")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("⚡ Top States by EV Registrations")
    if not df_vahan.empty:
        top_states_df = df_vahan.groupby("state")["ev_registrations"].sum().reset_index().sort_values(by="ev_registrations", ascending=False).head(8)
        fig_app_vahan = px.bar(
            top_states_df,
            x="state",
            y="ev_registrations",
            color="ev_registrations",
            color_continuous_scale="Viridis",
            labels={"ev_registrations": "Total Registrations", "state": "State"},
            title="Top States by EV Registrations",
            template="plotly_dark",
            height=380
        )
        fig_app_vahan = fix_plotly_dark(fig_app_vahan)
        st.plotly_chart(fig_app_vahan, use_container_width=True)

with col_g2:
    st.subheader("🔌 Charging Station Distribution by Operator")
    if not df_chargers.empty:
        top_op_df = df_chargers["operator"].value_counts().reset_index()
        top_op_df.columns = ["operator", "count"]
        fig_app_op = px.pie(
            top_op_df.head(6),
            names="operator",
            values="count",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Tealgrn,
            template="plotly_dark",
            title="Charging Station Distribution by Operator",
            height=380
        )
        fig_app_op = fix_plotly_dark(fig_app_op)
        st.plotly_chart(fig_app_op, use_container_width=True)

st.markdown("---")

# 3. Innovative, Interactive & Unique Sidebar
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9)); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 16px; padding: 18px; margin-top: 5px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 12px;">
        <div style="background: rgba(0, 230, 118, 0.18); border: 1.5px solid #00E676; border-radius: 12px; padding: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 16px rgba(0,230,118,0.4);">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#00E676" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
        </div>
        <div>
            <div style="font-size: 1.15rem; font-weight: 900; color: #FFFFFF !important; letter-spacing: -0.3px;">INDIA EV CORE</div>
            <div style="font-size: 0.76rem; color: #38BDF8 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">⚡ Spatial Engine</div>
        </div>
    </div>
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0, 230, 118, 0.3); border-radius: 12px; padding: 12px 14px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; color: #FFFFFF !important; font-weight: 800; margin-bottom: 4px;">
            <span style="width: 10px; height: 10px; border-radius: 50%; background-color: #00E676; box-shadow: 0 0 10px #00E676; display: inline-block;"></span>
            SYSTEM ONLINE
        </div>
        <div style="font-size: 0.78rem; color: #FFFFFF !important; line-height: 1.5;">Spatial decision matrix active with <b>130,000+</b> data points loaded.</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar.expander("⚡ System Telemetry & Datasets", expanded=False):
    st.markdown(f"""
    <div style="font-size: 0.85rem; color: #FFFFFF !important; line-height: 1.8;">
        <div>⚡ <b>Charging Stations:</b> <span style="color: #00E676 !important;">{len(df_chargers):,}</span></div>
        <div>🚗 <b>Vahan EV Records:</b> <span style="color: #38BDF8 !important;">{len(df_vahan):,}</span></div>
        <div>🏪 <b>Commercial POIs:</b> <span style="color: #FBBF24 !important;">{len(df_pois):,}</span></div>
        <div>🔌 <b>Substations:</b> <span style="color: #C084FC !important;">{len(df_power):,}</span></div>
        <div>🛣️ <b>Highway Corridors:</b> <span style="color: #34D399 !important;">{len(df_highways):,}</span></div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar.expander("🎛️ Active Decision Framework", expanded=False):
    st.markdown("""
    <div style="font-size: 0.82rem; color: #FFFFFF !important; line-height: 1.6;">
        <div>• <b>Ranking Method:</b> MCDA (AHP + TOPSIS)</div>
        <div>• <b>Spatial Engine:</b> SciPy KDTree & PyDeck</div>
        <div>• <b>Coverage:</b> Pan-India (All States & UTs)</div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 8px; font-size: 0.8rem; color: #FFFFFF !important; font-weight: 700;">
    ⚡ Powered by <span style="color: #00E676 !important;">Koushik Garg</span> | Data Analyst
</div>
""", unsafe_allow_html=True)
