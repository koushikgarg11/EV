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
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

try:
    from src.database.db_manager import db
except Exception:
    from database.db_manager import db

try:
    from src.gis_engine.catchment import CatchmentAnalyzer
    from src.gis_engine.hotspot import ChargingDesertHotspotAnalyzer
except Exception:
    from gis_engine.catchment import CatchmentAnalyzer
    from gis_engine.hotspot import ChargingDesertHotspotAnalyzer

try:
    from src.components import render_key_insights, apply_custom_theme, fix_plotly_dark
except Exception:
    try:
        from components import render_key_insights, apply_custom_theme, fix_plotly_dark
    except Exception:
        def apply_custom_theme():
            pass
        def fix_plotly_dark(fig):
            if fig is not None:
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"))
            return fig
        def render_key_insights(title="💡 Key Insights", insights=None, badge_text="⚡ EXECUTIVE METRICS", **kwargs):
            if insights is None:
                insights = ["No key insights available."]
            items = "".join([f"<div style='color:#FFFFFF !important;'><b>{i}</b></div>" for i in insights])
            st.markdown(f"<div style='padding:16px;border:1px solid rgba(56,189,248,0.3);border-radius:12px;background:#0f1724;color:#FFFFFF !important;'>{items}</div>", unsafe_allow_html=True)


st.set_page_config(page_title="Charging Desert Analysis", page_icon="🌵", layout="wide")

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
        padding: 6px !important;
        width: 100% !important;
        overflow: visible !important;
    }
</style>
""", unsafe_allow_html=True)

try:
    apply_custom_theme()
except Exception:
    pass

st.title("🌵 Charging Desert Hotspot Detection")
st.markdown("### *Automated spatial identification of high commercial demand zones lacking public EV chargers.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_pois = db.load_raw_dataset("points_of_interest")

@st.cache_data
def get_charging_deserts():
    pois_catchment = CatchmentAnalyzer.calculate_catchment_coverage(df_pois, df_chargers)
    deserts_df = ChargingDesertHotspotAnalyzer.identify_charging_deserts(pois_catchment, min_footfall=20, max_chargers_5km=2)
    return deserts_df

deserts_all = get_charging_deserts()

st.sidebar.header("🌵 Desert Sensitivity Parameters")
selected_state = st.sidebar.selectbox("Filter State", ["All States"] + list(deserts_all["state"].unique()))
min_footfall_slider = st.sidebar.slider("Minimum Footfall Index Threshold", 10, 100, 35, 5)
max_chargers_slider = st.sidebar.slider("Max Allowed Chargers within 5km", 0, 3, 1, 1)

deserts_filtered = deserts_all[
    (deserts_all["footfall_index"] >= min_footfall_slider) &
    (deserts_all["chargers_within_5km"] <= max_chargers_slider)
].copy()

if selected_state != "All States":
    deserts_filtered = deserts_filtered[deserts_filtered["state"] == selected_state]

deserts_only = deserts_filtered.sort_values(by="desert_severity_index", ascending=False)

# Metric Strip
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Identified Charging Deserts", f"{len(deserts_only):,}", delta="Critical Infra Gaps")
with col_m2:
    avg_dist = round(deserts_only['dist_nearest_charger_km'].mean(), 1) if not deserts_only.empty else 0.0
    st.metric("Avg Dist to Nearest Charger", f"{avg_dist} km", delta="Range Anxiety Zone", delta_color="inverse")
with col_m3:
    avg_severity = round(deserts_only['desert_severity_index'].mean(), 1) if not deserts_only.empty else 0.0
    st.metric("Avg Severity Index", f"{avg_severity} / 100", delta="Priority Score")
with col_m4:
    total_footfall = deserts_only['footfall_index'].sum() if not deserts_only.empty else 0
    st.metric("Total Unserved Footfall", f"{total_footfall:,}", delta="Unmet Demand Scale")

st.markdown("---")

# Visual Row 1: Severity Histogram & Footfall vs Distance Scatter
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Desert Severity Distribution")
    fig_hist = px.histogram(
        deserts_only,
        x="desert_severity_index",
        nbins=20,
        color_discrete_sequence=["#FF5252"],
        labels={"desert_severity_index": "Desert Severity Score"},
        template="plotly_dark",
        title="Desert Severity Distribution",
        height=400
    )
    fig_hist = fix_plotly_dark(fig_hist)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("🎯 Footfall Index vs Charger Distance Scatter")
    fig_scatter = px.scatter(
        deserts_only,
        x="dist_nearest_charger_km",
        y="footfall_index",
        color="desert_severity_index",
        size="footfall_index",
        color_continuous_scale="Reds",
        hover_name="name",
        hover_data=["category", "state", "district"],
        labels={"dist_nearest_charger_km": "Distance to Charger (km)", "footfall_index": "Commercial Footfall Index"},
        template="plotly_dark",
        title="Footfall Index vs Charger Distance Scatter",
        height=400
    )
    fig_scatter = fix_plotly_dark(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)


st.markdown("---")

# Visual Row 2: Interactive Folium Desert Map & Table
col_map, col_table = st.columns([1.2, 1])

with col_map:
    st.subheader("📍 Interactive Desert Hotspot Map (Folium)")
    if not deserts_only.empty:
        center_lat = float(deserts_only["lat"].mean())
        center_lon = float(deserts_only["lon"].mean())
    else:
        center_lat, center_lon = 20.5937, 78.9629

    m_desert = folium.Map(location=[center_lat, center_lon], zoom_start=5 if selected_state == "All States" else 7, tiles="CartoDB dark_matter")
    
    sample_deserts = deserts_only.head(200)
    for _, row in sample_deserts.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6 + (row["desert_severity_index"] / 15),
            color="#FF1744",
            fill=True,
            fill_color="#FF5252",
            fill_opacity=0.7,
            popup=f"<b>{row['name']}</b><br>State: {row['state']}<br>Category: {row['category']}<br>Dist to Charger: <b>{row['dist_nearest_charger_km']:.1f} km</b><br>Severity: <b>{row['desert_severity_index']:.1f}/100</b>"
        ).add_to(m_desert)
        
    st_folium(m_desert, use_container_width=True, height=450)

with col_table:
    st.subheader("🏆 Top Critical Charging Desert Hotspots")
    st.dataframe(
        deserts_only[["poi_id", "name", "category", "state", "district", "footfall_index", "dist_nearest_charger_km", "desert_severity_index"]].head(15).style.background_gradient(cmap="Reds", subset=["desert_severity_index"]),
        width="stretch",
        height=450
    )

st.markdown("---")

num_deserts = len(deserts_only)
render_key_insights(
    title="💡 Key Insights & Priority Action Takeaways",
    insights=[
        f"<b>High Commercial Demand Inequity:</b> Identified <span class='highlight-amber'>{num_deserts:,} charging desert hotspots</span> with high footfall but zero charger coverage within 5 km.",
        f"<b>Average Isolation Distance:</b> Deserts exhibit an average isolation distance of <span class='highlight-purple'>{avg_dist:.1f} km</span> to nearest station, causing range anxiety.",
        "<b>Deployment Priority:</b> High-footfall shopping centers and transit hubs represent prime opportunities for turn-key PPP charging station installations."
    ],
    badge_text="⚡ DESERT SEVERITY AUDIT"
)
