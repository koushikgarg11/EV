import os
import sys

# Ensure root directory is in sys.path for robust imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.gis_engine.network import NetworkCorridorAnalyzer
from src.components import render_key_insights

st.set_page_config(page_title="Highway Corridor Readiness", page_icon="🛣️", layout="wide")

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
    st.plotly_chart(fig_status, width="stretch")

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
    st.plotly_chart(fig_scatter, width="stretch")

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
st.plotly_chart(fig_bar, width="stretch")

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

