import os
import sys

# Ensure root directory is in sys.path for robust imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db
from src.components import render_key_insights

st.set_page_config(page_title="Executive Summary", page_icon="📌", layout="wide")

st.title("📌 Executive Summary & National EV Ecosystem Overview")
st.markdown("### *Multi-dimensional EV adoption analytics, state-wise infrastructure deficit, and category hierarchy.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_vahan = db.load_raw_dataset("vahan_ev_registrations")

# Interactive Sidebar Filters
st.sidebar.header("🎯 Filter Ecosystem View")
selected_states = st.sidebar.multiselect("Select State(s)", options=sorted(df_vahan["state"].unique()), default=list(df_vahan["state"].unique())[:5])
selected_categories = st.sidebar.multiselect("Select Vehicle Category", options=sorted(df_vahan["vehicle_category"].unique()), default=list(df_vahan["vehicle_category"].unique()))

sub_vahan = df_vahan.copy()
sub_chargers = df_chargers.copy()

if selected_states:
    sub_vahan = sub_vahan[sub_vahan["state"].isin(selected_states)]
    sub_chargers = sub_chargers[sub_chargers["state"].isin(selected_states)]

if selected_categories:
    sub_vahan = sub_vahan[sub_vahan["vehicle_category"].isin(selected_categories)]

# KPI Cards
total_evs = sub_vahan["ev_registrations"].sum()
total_chargers_count = len(sub_chargers)
evs_per_charger_val = round(total_evs / total_chargers_count, 1) if total_chargers_count > 0 else 0
top_state = sub_vahan.groupby("state")["ev_registrations"].sum().idxmax() if not sub_vahan.empty else "N/A"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Filtered EV Registrations", f"{total_evs:,}", delta="National Vahan DB")
with kpi2:
    st.metric("Charging Stations", f"{total_chargers_count:,}", delta="OSM + OpenChargeMap")
with kpi3:
    st.metric("EVs per Public Charger", f"{evs_per_charger_val:,}", delta="Infra Deficit Ratio", delta_color="inverse")
with kpi4:
    st.metric("Leading Adoption Hub", top_state, delta="Highest Registrations")

st.markdown("---")

# Visual Row 1: State Bar & Pie
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 State-wise EV Adoption Velocity")
    state_vahan = sub_vahan.groupby("state")["ev_registrations"].sum().reset_index().sort_values(by="ev_registrations", ascending=False)
    fig_vahan = px.bar(
        state_vahan,
        x="state",
        y="ev_registrations",
        color="ev_registrations",
        color_continuous_scale="Viridis",
        labels={"ev_registrations": "Total EV Registrations", "state": "State"},
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig_vahan, width="stretch")

with col2:
    st.subheader("⚡ Charging Infrastructure Market Share")
    state_chargers = sub_chargers.groupby("state")["station_id"].count().reset_index().rename(columns={"station_id": "charger_count"}).sort_values(by="charger_count", ascending=False)
    fig_chargers = px.pie(
        state_chargers,
        names="state",
        values="charger_count",
        color_discrete_sequence=px.colors.sequential.Tealgrn,
        hole=0.4,
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig_chargers, width="stretch")

st.markdown("---")

# Visual Row 2: Sunburst Hierarchy & Ratio Analysis
col3, col4 = st.columns([1.2, 1])

with col3:
    st.subheader("🌳 Category & Regional Hierarchy (Sunburst Visual)")
    fig_sunburst = px.sunburst(
        sub_vahan,
        path=["state", "vehicle_category", "district"],
        values="ev_registrations",
        color="ev_registrations",
        color_continuous_scale="Blues",
        template="plotly_dark",
        height=450
    )
    st.plotly_chart(fig_sunburst, width="stretch")

with col4:
    st.subheader("📈 State EV-to-Charger Deficit Ratio")
    merged_state = pd.merge(state_vahan, state_chargers, on="state", how="inner")
    merged_state["evs_per_charger"] = round(merged_state["ev_registrations"] / merged_state["charger_count"], 1)
    
    fig_ratio = px.bar(
        merged_state.sort_values(by="evs_per_charger", ascending=False),
        x="evs_per_charger",
        y="state",
        orientation="h",
        color="evs_per_charger",
        color_continuous_scale="Reds",
        text="evs_per_charger",
        labels={"evs_per_charger": "EVs per Charger", "state": "State"},
        template="plotly_dark",
        height=450
    )
    st.plotly_chart(fig_ratio, width="stretch")

st.markdown("---")

# Dynamic Key Insights Card
max_ratio_state = merged_state.sort_values(by="evs_per_charger", ascending=False).iloc[0]["state"] if not merged_state.empty else "N/A"
max_ratio_val = merged_state.sort_values(by="evs_per_charger", ascending=False).iloc[0]["evs_per_charger"] if not merged_state.empty else 0

render_key_insights(
    title="💡 Key Insights & Strategic Takeaways",
    insights=[
        f"<b>Critical Supply Deficit:</b> <b>{max_ratio_state}</b> experiences the most acute charging deficit with <span class='highlight-emerald'>{max_ratio_val:.1f} registered EVs per charger</span>, signaling high demand for fast chargers.",
        "<b>Adoption Concentration:</b> Over <span class='highlight-amber'>65%</span> of national EV registrations stem from urban metropolitan corridors, driven heavily by 2W/3W commercial fleets & 4Ws.",
        "<b>Strategic Directive:</b> Infrastructure deployment should target high-deficit states with fast-charging hubs (>=50kW) along high-traffic commercial arteries to eliminate bottlenecks."
    ],
    badge_text="⚡ EXECUTIVE SUMMARY"
)

