import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.gis_engine.network import NetworkCorridorAnalyzer

st.set_page_config(page_title="Highway Corridor Readiness", page_icon="🛣️", layout="wide")

st.title("🛣️ National Highway Corridor Readiness Analysis")
st.markdown("### *Inter-city charging gap analysis along major National Highway routes (NH-48, NH-44, NH-65, etc.).*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_highways = db.load_raw_dataset("highway_corridors")

@st.cache_data
def analyze_corridors():
    return NetworkCorridorAnalyzer.analyze_corridor_readiness(df_highways, df_chargers)

df_analyzed = analyze_corridors()

st.sidebar.header("Corridor Filters")
selected_nh = st.sidebar.selectbox("National Highway Route", ["All Routes"] + list(df_analyzed["highway_name"].unique()))

if selected_nh != "All Routes":
    df_sub = df_analyzed[df_analyzed["highway_name"] == selected_nh]
else:
    df_sub = df_analyzed

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛣️ Highway Readiness Classification")
    status_counts = df_sub["readiness_status"].value_counts().reset_index()
    status_counts.columns = ["Readiness Status", "Segment Count"]
    fig_status = px.pie(
        status_counts,
        names="Readiness Status",
        values="Segment Count",
        color_discrete_sequence=["#FF5252", "#FFC107", "#00E676"],
        hole=0.4,
        template="plotly_dark"
    )
    st.plotly_chart(fig_status, use_container_width=True)

with col2:
    st.subheader("🚚 Daily Traffic Volume vs Nearest Charger Distance")
    fig_scatter = px.scatter(
        df_sub,
        x="daily_traffic_volume",
        y="nearest_charger_dist_km",
        color="corridor_gap_score",
        color_continuous_scale="Reds",
        size="freight_percentage",
        hover_data=["highway_id", "highway_name"],
        labels={"daily_traffic_volume": "Daily Traffic Volume", "nearest_charger_dist_km": "Distance to Charger (km)"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Priority Highway Segments for Investment
st.subheader("🚨 Priority Highway Investment Segments")
priority_segments = df_sub.sort_values(by="corridor_gap_score", ascending=False).head(15)

st.dataframe(
    priority_segments[["highway_id", "highway_name", "daily_traffic_volume", "freight_percentage", "nearest_charger_dist_km", "corridor_gap_score", "readiness_status"]],
    use_container_width=True
)
