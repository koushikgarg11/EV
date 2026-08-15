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

try:
    from src.database.db_manager import db
except Exception:
    from database.db_manager import db

try:
    from src.gis_engine.network import NetworkCorridorAnalyzer
except Exception:
    from gis_engine.network import NetworkCorridorAnalyzer

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


st.set_page_config(page_title="Highway Corridor Readiness", page_icon="🛣️", layout="wide")

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

st.title("🛣️ National Highway Corridor Readiness Analysis")
st.markdown("### *Inter-city charging gap analysis along major National Highway routes (NH-48, NH-44, NH-65, NH-16).*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_highways = db.load_raw_dataset("highway_corridors")

@st.cache_data
def analyze_corridors():
    return NetworkCorridorAnalyzer.analyze_corridor_readiness(df_highways, df_chargers)

df_analyzed = analyze_corridors()

st.sidebar.header("🎯 Corridor Filters")
selected_nh = st.sidebar.selectbox("National Highway Route", ["All Routes"] + list(df_analyzed["highway_name"].unique()))
status_filter = st.sidebar.multiselect("Readiness Status", options=sorted(df_analyzed["readiness_status"].unique()), default=list(df_analyzed["readiness_status"].unique()))

df_sub = df_analyzed.copy()
if selected_nh != "All Routes":
    df_sub = df_sub[df_sub["highway_name"] == selected_nh]
if status_filter:
    df_sub = df_sub[df_sub["readiness_status"].isin(status_filter)]

# KPI Strip
critical_count = len(df_sub[df_sub["readiness_status"] == "Critical Gap Zone"])
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Analyzed Highway Segments", f"{len(df_sub):,}", delta="National Highway Network")
with kpi2:
    st.metric("Critical Gap Segments", f"{critical_count:,}", delta="Immediate Action Needed", delta_color="inverse")
with kpi3:
    avg_traffic = round(df_sub["daily_traffic_volume"].mean(), 0) if not df_sub.empty else 0
    st.metric("Avg Daily Traffic", f"{avg_traffic:,.0f} Vehicles", delta="Corridor Throughput")
with kpi4:
    max_gap = round(df_sub["nearest_charger_dist_km"].max(), 1) if not df_sub.empty else 0
    st.metric("Max Charger Distance Gap", f"{max_gap} km", delta="Longest Unserved Stretch", delta_color="inverse")

st.markdown("---")

# Visual Row 1: Pie Classification & Traffic vs Charger Distance Scatter
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛣️ Highway Readiness Breakdown")
    status_counts = df_sub["readiness_status"].value_counts().reset_index()
    status_counts.columns = ["Readiness Status", "Segment Count"]
    fig_status = px.pie(
        status_counts,
        names="Readiness Status",
        values="Segment Count",
        color="Readiness Status",
        color_discrete_map={"Critical Gap Zone": "#FF5252", "Moderate Risk": "#FFC107", "Readiness High": "#00E676"},
        hole=0.4,
        template="plotly_dark",
        height=400
    )
    fig_status = fix_plotly_dark(fig_status)
    st.plotly_chart(fig_status, use_container_width=True)

with col2:
    st.subheader("🚚 Traffic Volume vs Charger Distance")
    fig_scatter = px.scatter(
        df_sub,
        x="daily_traffic_volume",
        y="nearest_charger_dist_km",
        color="corridor_gap_score",
        color_continuous_scale="Reds",
        size="freight_percentage",
        hover_name="highway_id",
        hover_data=["highway_name", "readiness_status", "freight_percentage"],
        labels={"daily_traffic_volume": "Daily Traffic Volume (Vehicles/Day)", "nearest_charger_dist_km": "Distance to Charger (km)"},
        template="plotly_dark",
        height=400
    )
    fig_scatter = fix_plotly_dark(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Visual Row 2: Route Profile Bar Chart
st.subheader("📈 Highway Gap Score Profile Across Segments")
fig_bar = px.bar(
    df_sub.sort_values(by="corridor_gap_score", ascending=False).head(20),
    x="highway_id",
    y="corridor_gap_score",
    color="readiness_status",
    color_discrete_map={"Critical Gap Zone": "#FF5252", "Moderate Risk": "#FFC107", "Readiness High": "#00E676"},
    text="nearest_charger_dist_km",
    labels={"corridor_gap_score": "Corridor Gap Risk Score", "highway_id": "Highway Segment ID"},
    template="plotly_dark",
    height=420
)
fig_bar = fix_plotly_dark(fig_bar)
st.plotly_chart(fig_bar, use_container_width=True)


st.markdown("---")

# Priority Highway Table
st.subheader("🚨 Priority Highway Investment Segments Matrix")
priority_segments = df_sub.sort_values(by="corridor_gap_score", ascending=False).head(15)

st.dataframe(
    priority_segments[["highway_id", "highway_name", "daily_traffic_volume", "freight_percentage", "nearest_charger_dist_km", "corridor_gap_score", "readiness_status"]].style.background_gradient(cmap="Reds", subset=["corridor_gap_score"]),
    width="stretch"
)

st.markdown("---")

render_key_insights(
    title="💡 Key Insights & Highway Investment Takeaways",
    insights=[
        f"<b>Inter-city Bottlenecks:</b> Out of analyzed highway segments, <span class='highlight-amber'>{critical_count} segments</span> are classified as <b>Critical Gap Zones</b> (>40 km spacing).",
        "<b>Freight Corridor Preparedness:</b> High-freight routes (>35% freight traffic) require MW-scale charging plazas for commercial electric trucks & heavy fleets.",
        "<b>High-ROI Investment Recommendation:</b> Priority funding should target NH-48 (Delhi-Mumbai) and NH-44 intersections to establish mega fast-charging corridors."
    ],
    badge_text="⚡ HIGHWAY GAP ANALYSIS"
)
