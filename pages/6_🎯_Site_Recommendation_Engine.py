import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.gis_engine.catchment import CatchmentAnalyzer
from src.decision_engine.mcda import MCDARecommendationEngine
from src.decision_engine.explainability import ExplainableRecommendationEngine

st.set_page_config(page_title="Site Recommendation Engine", page_icon="🎯", layout="wide")

st.title("🎯 Explainable EV Charging Site Recommendation Engine")
st.markdown("### *AHP & TOPSIS Multi-Criteria Decision Analysis ranking top priority locations with transparent score attribution.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_pois = db.load_raw_dataset("points_of_interest")

@st.cache_data
def get_recommendations():
    pois_catchment = CatchmentAnalyzer.calculate_catchment_coverage(df_pois, df_chargers)
    mcda = MCDARecommendationEngine()
    ranked_df = mcda.calculate_priority_scores(pois_catchment)
    return ranked_df

ranked_df = get_recommendations()

st.sidebar.header("Filter Recommendations")
selected_state = st.sidebar.selectbox("State Filter", ["All States"] + list(ranked_df["state"].unique()))
selected_category = st.sidebar.selectbox("POI Category", ["All Categories"] + list(ranked_df["category"].unique()))

sub_ranked = ranked_df.copy()
if selected_state != "All States":
    sub_ranked = sub_ranked[sub_ranked["state"] == selected_state]
if selected_category != "All Categories":
    sub_ranked = sub_ranked[sub_ranked["category"] == selected_category]

top_20 = sub_ranked.head(20)

st.subheader("🏆 Top 20 Recommended Investment Locations")

st.dataframe(
    top_20[["rank", "poi_id", "name", "category", "state", "district", "footfall_index", "dist_nearest_charger_km", "has_high_voltage_power", "priority_investment_score"]],
    use_container_width=True
)

st.markdown("---")

# Deep-dive Explainability Card
st.subheader("🔍 Explainable Site Breakdown & Score Attribution")
selected_site_name = st.selectbox("Select Candidate Location to Inspect:", top_20["name"].tolist())

selected_row = top_20[top_20["name"] == selected_site_name].iloc[0]
explanation = ExplainableRecommendationEngine.explain_recommendation(selected_row, MCDARecommendationEngine().weights)

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.markdown(f"""
    <div style="background: rgba(22, 27, 34, 0.8); border: 1px solid #00E676; border-radius: 12px; padding: 20px;">
        <h3>📍 {explanation['name']}</h3>
        <p><b>Site ID:</b> {explanation['site_id']}</p>
        <p><b>Priority Investment Score:</b> <span style="color:#00E676; font-size:1.5rem; font-weight:bold;">{explanation['total_score']} / 100</span></p>
        <p><b>Confidence Index:</b> <span style="color:#FFC107; font-weight:bold;">{explanation['confidence_score']}%</span></p>
        <p><b>Primary Investment Driver:</b> <span style="color:#00B0FF; font-weight:bold;">{explanation['primary_driver']}</span></p>
    </div>
    """, unsafe_allow_html=True)

with col_exp2:
    contrib_data = pd.DataFrame({
        "Criteria": ["Commercial Demand", "Charging Desert Gap", "Grid & Power Readiness", "Parking Capacity"],
        "Contribution %": [explanation["demand_contrib_pct"], explanation["charging_gap_contrib_pct"], explanation["grid_readiness_contrib_pct"], explanation["capacity_contrib_pct"]]
    })
    
    fig_contrib = px.bar(
        contrib_data,
        x="Criteria",
        y="Contribution %",
        color="Criteria",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="Contribution %",
        template="plotly_dark"
    )
    st.plotly_chart(fig_contrib, use_container_width=True)
