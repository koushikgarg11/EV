import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db

st.set_page_config(page_title="Executive Summary", page_icon="📌", layout="wide")

st.title("📌 Executive Summary & EV Ecosystem Overview")
st.markdown("### *National EV adoption overview, state-wise distribution, and charger density metrics.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_vahan = db.load_raw_dataset("vahan_ev_registrations")

# Top State EV Registrations
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 State-wise Vahan EV Registrations")
    state_vahan = df_vahan.groupby("state")["ev_registrations"].sum().reset_index().sort_values(by="ev_registrations", ascending=False)
    fig_vahan = px.bar(
        state_vahan,
        x="state",
        y="ev_registrations",
        color="ev_registrations",
        color_continuous_scale="Viridis",
        labels={"ev_registrations": "Total EV Registrations", "state": "State"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_vahan, use_container_width=True)

with col2:
    st.subheader("⚡ State-wise Charging Station Count")
    state_chargers = df_chargers.groupby("state")["station_id"].count().reset_index().rename(columns={"station_id": "charger_count"}).sort_values(by="charger_count", ascending=False)
    fig_chargers = px.pie(
        state_chargers,
        names="state",
        values="charger_count",
        color_discrete_sequence=px.colors.sequential.Tealgrn,
        hole=0.4,
        template="plotly_dark"
    )
    st.plotly_chart(fig_chargers, use_container_width=True)

st.markdown("---")

# EV Charger Ratio by State
st.subheader("📈 State EV-to-Charger Ratio Comparison")
merged_state = pd.merge(state_vahan, state_chargers, on="state")
merged_state["evs_per_charger"] = round(merged_state["ev_registrations"] / merged_state["charger_count"], 1)

fig_ratio = px.bar(
    merged_state.sort_values(by="evs_per_charger", ascending=False),
    x="state",
    y="evs_per_charger",
    color="evs_per_charger",
    color_continuous_scale="Reds",
    text="evs_per_charger",
    labels={"evs_per_charger": "Registered EVs per Public Charger", "state": "State"},
    template="plotly_dark"
)
st.plotly_chart(fig_ratio, use_container_width=True)

st.markdown("""
<div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(48, 54, 61, 0.8); border-radius: 12px; padding: 18px; margin-top: 15px;">
    <h4>💡 Key Insight</h4>
    <p>A higher <b>EVs per Public Charger</b> ratio indicates a severe infrastructure gap where EV adoption is outpacing public charging deployment. States like Maharashtra and Delhi exhibit high registration volumes requiring urgent high-power fast charger installations.</p>
</div>
""", unsafe_allow_html=True)
