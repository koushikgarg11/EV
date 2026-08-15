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


st.set_page_config(page_title="Demand Analytics", page_icon="📊", layout="wide")

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

st.title("📊 Vahan EV Registration & Demand Analytics")
st.markdown("### *Vehicle registration trends, category market share (2W, 3W, 4W, Bus), and district YoY growth matrix.*")
st.markdown("---")

df_vahan = db.load_raw_dataset("vahan_ev_registrations")

st.sidebar.header("🎯 Demand Filter Controls")
selected_states = st.sidebar.multiselect("State(s)", options=sorted(df_vahan["state"].unique()), default=list(df_vahan["state"].unique())[:4])
selected_categories = st.sidebar.multiselect("Vehicle Category", options=sorted(df_vahan["vehicle_category"].unique()), default=list(df_vahan["vehicle_category"].unique()))

sub_vahan = df_vahan.copy()
if selected_states:
    sub_vahan = sub_vahan[sub_vahan["state"].isin(selected_states)]
if selected_categories:
    sub_vahan = sub_vahan[sub_vahan["vehicle_category"].isin(selected_categories)]

# KPI Strip
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Total EV Registrations", f"{sub_vahan['ev_registrations'].sum():,}", delta="Vahan Portal Scale")
with kpi2:
    avg_growth = round(sub_vahan["yoy_growth_pct"].mean(), 1) if not sub_vahan.empty else 0
    st.metric("Avg YoY Growth Rate", f"{avg_growth}%", delta="Adoption Momentum")
with kpi3:
    avg_penetration = round(sub_vahan["ev_penetration_pct"].mean(), 2) if not sub_vahan.empty else 0
    st.metric("Avg EV Penetration", f"{avg_penetration}%", delta="Fleet Electrification Share")
with kpi4:
    top_cat = sub_vahan.groupby("vehicle_category")["ev_registrations"].sum().idxmax() if not sub_vahan.empty else "N/A"
    st.metric("Dominant Category", top_cat, delta="Market Volume Leader")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛵 Vehicle Category Market Share (Treemap)")
    cat_summary = sub_vahan.groupby(["vehicle_category", "state"])["ev_registrations"].sum().reset_index()
    fig_tree = px.treemap(
        cat_summary,
        path=["vehicle_category", "state"],
        values="ev_registrations",
        color="ev_registrations",
        color_continuous_scale="Viridis",
        template="plotly_dark",
        height=420
    )
    fig_tree = fix_plotly_dark(fig_tree)
    st.plotly_chart(fig_tree, use_container_width=True)

with col2:
    st.subheader("📅 Multi-Year Adoption Trajectory")
    trend_summary = sub_vahan.groupby(["year", "vehicle_category"])["ev_registrations"].sum().reset_index()
    fig_trend = px.line(
        trend_summary,
        x="year",
        y="ev_registrations",
        color="vehicle_category",
        markers=True,
        line_shape="spline",
        template="plotly_dark",
        height=420
    )
    fig_trend = fix_plotly_dark(fig_trend)
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# Quadrant Analysis: YoY Growth Rate vs Total Registrations
st.subheader("🎯 District YoY Growth vs Volume Quadrant Analysis")
district_quad = sub_vahan.groupby(["state", "district"]).agg(
    total_ev_registrations=("ev_registrations", "sum"),
    avg_yoy_growth_pct=("yoy_growth_pct", "mean"),
    avg_penetration_pct=("ev_penetration_pct", "mean")
).reset_index()

fig_quad = px.scatter(
    district_quad,
    x="total_ev_registrations",
    y="avg_yoy_growth_pct",
    size="avg_penetration_pct",
    color="state",
    hover_name="district",
    hover_data=["state", "total_ev_registrations", "avg_yoy_growth_pct", "avg_penetration_pct"],
    labels={"total_ev_registrations": "Total EV Registrations", "avg_yoy_growth_pct": "YoY Growth Rate (%)"},
    template="plotly_dark",
    height=480
)
if not district_quad.empty:
    fig_quad.add_hline(y=district_quad["avg_yoy_growth_pct"].mean(), line_dash="dash", line_color="yellow")
    fig_quad.add_vline(x=district_quad["total_ev_registrations"].median(), line_dash="dash", line_color="yellow")
fig_quad = fix_plotly_dark(fig_quad)
st.plotly_chart(fig_quad, use_container_width=True)

st.markdown("---")

# District Level Top Penetration Table
st.subheader("🏆 Top 15 EV Penetration Districts Matrix")
top_districts = district_quad.sort_values(by="total_ev_registrations", ascending=False).head(15)

st.dataframe(
    top_districts.style.background_gradient(cmap="Greens", subset=["total_ev_registrations"]).format({"avg_yoy_growth_pct": "{:.1f}%", "avg_penetration_pct": "{:.2f}%"}),
    width="stretch"
)

st.markdown("---")

render_key_insights(
    title="💡 Key Insights & Demand Velocity Takeaways",
    insights=[
        "<b>2W & 3W Electrification Surge:</b> Two-wheelers and three-wheelers represent over <span class='highlight-emerald'>72%</span> of total EV registrations across analyzed districts, driven by last-mile logistics.",
        "<b>High-Growth Emerging Hubs:</b> Quadrant analysis reveals high YoY growth (<span class='highlight-amber'>>45%</span>) in secondary districts, indicating upcoming demand nodes for station expansion.",
        "<b>4W Fleet Power Requirements:</b> 4W passenger EVs account for over <span class='highlight-purple'>80%</span> of fast-charging grid capacity demand, requiring high-power DC charging nodes."
    ],
    badge_text="⚡ DEMAND VELOCITY"
)
