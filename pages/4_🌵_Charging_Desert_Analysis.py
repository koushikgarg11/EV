import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.gis_engine.catchment import CatchmentAnalyzer
from src.gis_engine.hotspot import ChargingDesertHotspotAnalyzer

st.set_page_config(page_title="Charging Desert Analysis", page_icon="🌵", layout="wide")

st.title("🌵 Charging Desert Hotspot Detection")
st.markdown("### *Automated spatial identification of high commercial demand zones lacking public EV chargers.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_pois = db.load_raw_dataset("points_of_interest")

@st.cache_data
def get_charging_deserts():
    pois_catchment = CatchmentAnalyzer.calculate_catchment_coverage(df_pois, df_chargers)
    deserts_df = ChargingDesertHotspotAnalyzer.identify_charging_deserts(pois_catchment, min_footfall=40, max_chargers_5km=1)
    return deserts_df

deserts_all = get_charging_deserts()
deserts_only = deserts_all[deserts_all["is_charging_desert"]].sort_values(by="desert_severity_index", ascending=False)

col_metric1, col_metric2, col_metric3 = st.columns(3)

with col_metric1:
    st.metric("Total Identified Charging Deserts", f"{len(deserts_only):,}", delta="Critical Gap Zones")
with col_metric2:
    st.metric("Avg Distance to Nearest Charger", f"{deserts_only['dist_nearest_charger_km'].mean():.1f} km", delta="High Range Anxiety")
with col_metric3:
    st.metric("Avg Severity Index", f"{deserts_only['desert_severity_index'].mean():.1f} / 100", delta="Priority Action Needed")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Charging Desert Severity Distribution")
    fig_hist = px.histogram(
        deserts_only,
        x="desert_severity_index",
        nbins=20,
        color_discrete_sequence=["#FF5252"],
        labels={"desert_severity_index": "Desert Severity Score"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("📍 Top Severe Charging Desert Hotspots")
    st.dataframe(
        deserts_only[["poi_id", "name", "category", "state", "district", "footfall_index", "dist_nearest_charger_km", "desert_severity_index"]].head(15),
        use_container_width=True
    )
