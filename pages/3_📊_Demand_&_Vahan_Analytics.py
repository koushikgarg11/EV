import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.db_manager import db

st.set_page_config(page_title="Demand Analytics", page_icon="📊", layout="wide")

st.title("📊 Vahan EV Registration & Demand Analytics")
st.markdown("### *Vehicle registration trends, category breakdowns (2W, 3W, 4W, Bus), and YoY growth analysis.*")
st.markdown("---")

df_vahan = db.load_raw_dataset("vahan_ev_registrations")

st.sidebar.header("Filter Criteria")
selected_state = st.sidebar.selectbox("State", ["All"] + list(df_vahan["state"].unique()))
selected_category = st.sidebar.selectbox("Vehicle Category", ["All Categories"] + list(df_vahan["vehicle_category"].unique()))

sub_vahan = df_vahan.copy()
if selected_state != "All":
    sub_vahan = sub_vahan[sub_vahan["state"] == selected_state]
if selected_category != "All Categories":
    sub_vahan = sub_vahan[sub_vahan["vehicle_category"] == selected_category]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛵 Vehicle Category Share")
    cat_summary = sub_vahan.groupby("vehicle_category")["ev_registrations"].sum().reset_index()
    fig_cat = px.bar(
        cat_summary,
        x="vehicle_category",
        y="ev_registrations",
        color="vehicle_category",
        color_discrete_sequence=px.colors.qualitative.Bold,
        text="ev_registrations",
        labels={"ev_registrations": "Registrations", "vehicle_category": "Category"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    st.subheader("📅 Multi-Year Adoption Growth Trend")
    trend_summary = sub_vahan.groupby(["year", "vehicle_category"])["ev_registrations"].sum().reset_index()
    fig_trend = px.line(
        trend_summary,
        x="year",
        y="ev_registrations",
        color="vehicle_category",
        markers=True,
        template="plotly_dark"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# District Level Top Penetration Table
st.subheader("🏆 Top 15 EV Penetration Districts")
district_summary = sub_vahan.groupby(["state", "district"]).agg(
    total_ev_registrations=("ev_registrations", "sum"),
    avg_penetration_pct=("ev_penetration_pct", "mean"),
    avg_yoy_growth_pct=("yoy_growth_pct", "mean")
).reset_index().sort_values(by="total_ev_registrations", ascending=False).head(15)

st.dataframe(
    district_summary.style.background_gradient(cmap="Blues", subset=["total_ev_registrations"]),
    use_container_width=True
)
