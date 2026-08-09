import os
import sys

# Ensure root directory is in sys.path for robust imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.gis_engine.catchment import CatchmentAnalyzer
from src.decision_engine.simulator import ScenarioSimulatorEngine
from src.components import render_key_insights

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

st.sidebar.header("🎯 Preset Strategy Profiles")
preset_strategy = st.sidebar.selectbox(
    "Select Strategy Preset",
    ["Custom Manual", "Demand-First Focus", "Grid Substation Heavy", "Highway Gap Primary", "Balanced Strategy"]
)

# Preset weights mapping
if preset_strategy == "Demand-First Focus":
    default_d, default_g, default_i, default_c = 0.55, 0.15, 0.15, 0.15
elif preset_strategy == "Grid Substation Heavy":
    default_d, default_g, default_i, default_c = 0.15, 0.15, 0.55, 0.15
elif preset_strategy == "Highway Gap Primary":
    default_d, default_g, default_i, default_c = 0.15, 0.55, 0.15, 0.15
elif preset_strategy == "Balanced Strategy":
    default_d, default_g, default_i, default_c = 0.25, 0.25, 0.25, 0.25
else:
    default_d, default_g, default_i, default_c = 0.35, 0.25, 0.20, 0.20

st.sidebar.header("🎛️ Customize Weight Factors")
w_demand = st.sidebar.slider("Commercial & EV Demand Weight", 0.0, 1.0, default_d, 0.05)
w_gap = st.sidebar.slider("Charging Desert Gap Weight", 0.0, 1.0, default_g, 0.05)
w_infra = st.sidebar.slider("Grid & Substation Weight", 0.0, 1.0, default_i, 0.05)
w_capacity = st.sidebar.slider("Parking & Accessibility Weight", 0.0, 1.0, default_c, 0.05)

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
**Normalized Strategy Breakdown:**
- Commercial Demand: `{custom_weights['demand_weight']*100:.0f}%`
- Desert Gap: `{custom_weights['gap_weight']*100:.0f}%`
- Substation Grid: `{custom_weights['infrastructure_weight']*100:.0f}%`
- Parking & Highway: `{custom_weights['corridor_weight']*100:.0f}%`
""")

simulated_top20 = ScenarioSimulatorEngine.run_simulation(pois_catchment, custom_weights=custom_weights, top_n=20)

# KPI Strip
col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1:
    st.metric("Active Strategy Profile", preset_strategy)
with col_k2:
    st.metric("Top Simulated Site", simulated_top20.iloc[0]["name"] if not simulated_top20.empty else "N/A")
with col_k3:
    sim_top_score = simulated_top20.iloc[0]["priority_investment_score"] if not simulated_top20.empty else 0
    st.metric("Top Simulated Score", f"{sim_top_score:.1f} / 100")
with col_k4:
    st.metric("Analyzed Candidate Scale", f"{len(pois_catchment):,} POIs")

st.markdown("---")

# Visual Section 1: Simulated Priority Bar Chart
st.subheader("⚡ Simulated Priority Site Rankings under Active Strategy Profile")

fig_sim = px.bar(
    simulated_top20,
    x="name",
    y="priority_investment_score",
    color="priority_investment_score",
    color_continuous_scale="Viridis",
    text="priority_investment_score",
    labels={"priority_investment_score": "Simulated Priority Score", "name": "Location Name"},
    template="plotly_dark",
    height=420
)
st.plotly_chart(fig_sim, width="stretch")

st.markdown("---")

# Visual Section 2: Parallel Coordinates Plot for MCDA Trade-offs
st.subheader("🔀 Parallel Coordinates Multi-Criteria Trade-off Analysis")

# Convert boolean grid column to numeric for parallel coordinates
para_df = simulated_top20.copy()
para_df["grid_numeric"] = para_df["has_high_voltage_power"].astype(int)

fig_para = px.parallel_coordinates(
    para_df,
    dimensions=["footfall_index", "dist_nearest_charger_km", "grid_numeric", "priority_investment_score"],
    color="priority_investment_score",
    color_continuous_scale="Tealgrn",
    labels={
        "footfall_index": "Footfall Index",
        "dist_nearest_charger_km": "Nearest Charger Dist (km)",
        "grid_numeric": "High Voltage Grid (1/0)",
        "priority_investment_score": "Priority Score"
    },
    template="plotly_dark",
    height=450
)
st.plotly_chart(fig_para, width="stretch")

st.markdown("---")

# Table
st.subheader("📋 Detailed Simulated Priority Matrix")
st.dataframe(
    simulated_top20[["rank", "poi_id", "name", "category", "state", "district", "footfall_index", "dist_nearest_charger_km", "has_high_voltage_power", "priority_investment_score"]].style.background_gradient(cmap="Blues", subset=["priority_investment_score"]),
    width="stretch"
)

st.markdown("---")

render_key_insights(
    title="💡 Key Insights & Sensitivity Analysis Takeaways",
    insights=[
        f"<b>Strategy Sensitivity:</b> Under <b>{preset_strategy}</b>, top-tier candidate sites shift based on grid proximity versus footfall density, emphasizing multi-scenario stress testing.",
        "<b>Parallel Coordinates Trade-off:</b> Locations with high grid readiness maintain high priority scores even when demand weights decrease, demonstrating resilience.",
        "<b>Decision Recommendation:</b> Highly resilient sites that remain in the Top 10 across all 5 strategy presets represent <span class='highlight-emerald'>low-risk investment targets</span>."
    ],
    badge_text="⚡ SCENARIO SIMULATION"
)

