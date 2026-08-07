import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.gis_engine.catchment import CatchmentAnalyzer
from src.decision_engine.simulator import ScenarioSimulatorEngine

st.set_page_config(page_title="Scenario Simulator", page_icon="🎛️", layout="wide")

st.title("🎛️ Interactive What-If Scenario Simulator")
st.markdown("### *Simulate site recommendations by dynamically adjusting multi-criteria weights in real-time.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_pois = db.load_raw_dataset("points_of_interest")

@st.cache_data
def get_pois_with_catchment():
    return CatchmentAnalyzer.calculate_catchment_coverage(df_pois, df_chargers)

pois_catchment = get_pois_with_catchment()

st.sidebar.header("🎛️ Customize Weight Factors")
w_demand = st.sidebar.slider("Commercial & EV Demand Weight", 0.0, 1.0, 0.35, 0.05)
w_gap = st.sidebar.slider("Charging Desert Gap Weight", 0.0, 1.0, 0.25, 0.05)
w_infra = st.sidebar.slider("Grid & Substation Readiness Weight", 0.0, 1.0, 0.20, 0.05)
w_capacity = st.sidebar.slider("Parking & Highway Accessibility Weight", 0.0, 1.0, 0.20, 0.05)

# Normalize weights
total_w = w_demand + w_gap + w_infra + w_capacity
if total_w > 0:
    custom_weights = {
        "demand_weight": round(w_demand / total_w, 2),
        "gap_weight": round(w_gap / total_w, 2),
        "infrastructure_weight": round(w_infra / total_w, 2),
        "corridor_weight": round(w_capacity / total_w, 2)
    }
else:
    custom_weights = {"demand_weight": 0.25, "gap_weight": 0.25, "infrastructure_weight": 0.25, "corridor_weight": 0.25}

st.sidebar.markdown(f"""
**Normalized Weights Breakdown:**
- Demand: `{custom_weights['demand_weight']*100:.0f}%`
- Gap: `{custom_weights['gap_weight']*100:.0f}%`
- Grid: `{custom_weights['infrastructure_weight']*100:.0f}%`
- Parking: `{custom_weights['corridor_weight']*100:.0f}%`
""")

simulated_top20 = ScenarioSimulatorEngine.run_simulation(pois_catchment, custom_weights=custom_weights, top_n=20)

st.subheader("⚡ Simulated Priority Site Rankings under Custom Weights")

fig_sim = px.bar(
    simulated_top20,
    x="name",
    y="priority_investment_score",
    color="priority_investment_score",
    color_continuous_scale="Viridis",
    text="priority_investment_score",
    labels={"priority_investment_score": "Simulated Priority Score", "name": "Location Name"},
    template="plotly_dark"
)
st.plotly_chart(fig_sim, use_container_width=True)

st.dataframe(
    simulated_top20[["rank", "poi_id", "name", "category", "state", "district", "footfall_index", "dist_nearest_charger_km", "priority_investment_score"]],
    use_container_width=True
)
