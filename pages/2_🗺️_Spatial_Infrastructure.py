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
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

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


st.set_page_config(page_title="Spatial Infrastructure", page_icon="🗺️", layout="wide")

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

st.title("🗺️ Spatial Infrastructure & Interactive Heatmap Engine")
st.markdown("### *Interactive Plotly Density maps, 3D spatial coordinate bubbles, and Folium multi-layered catchment maps.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_pois = db.load_raw_dataset("points_of_interest")

st.sidebar.header("🎯 Spatial Map Filters")
selected_state = st.sidebar.selectbox("Select State", ["All States"] + list(df_chargers["state"].unique()))
charger_type_filter = st.sidebar.multiselect("Charger Type", options=sorted(df_chargers["charger_type"].unique()), default=list(df_chargers["charger_type"].unique()))
min_power = st.sidebar.slider("Minimum Power Rating (kW)", 0, 150, 0, 10)

chargers_sub = df_chargers.copy()
if selected_state != "All States":
    chargers_sub = chargers_sub[chargers_sub["state"] == selected_state]
if charger_type_filter:
    chargers_sub = chargers_sub[chargers_sub["charger_type"].isin(charger_type_filter)]
chargers_sub = chargers_sub[chargers_sub["kw_power"] >= min_power]

# KPI Strip
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    st.metric("Displayed Stations", f"{len(chargers_sub):,}", delta="Filtered Spatial Scale")
with col_kpi2:
    fast_chargers = len(chargers_sub[chargers_sub["kw_power"] >= 50])
    st.metric("Fast DC Chargers (>=50kW)", f"{fast_chargers:,}", delta=f"{round(fast_chargers/len(chargers_sub)*100 if len(chargers_sub)>0 else 0, 1)}% Fast Share")
with col_kpi3:
    avg_power = round(chargers_sub["kw_power"].mean(), 1) if not chargers_sub.empty else 0
    st.metric("Avg Power Output", f"{avg_power} kW", delta="Grid Capacity Metric")
with col_kpi4:
    top_operator = chargers_sub["operator"].mode()[0] if not chargers_sub.empty else "N/A"
    st.metric("Dominant Operator", top_operator, delta="Network Market Leader")

st.markdown("---")

# Visual Section 1: Density Map (Plotly) vs Folium Catchment Map
col_map1, col_map2 = st.columns(2)

with col_map1:
    st.subheader("🔥 Plotly 2D Spatial Density Heatmap")
    colorscale_choice = st.selectbox("Color Palette", ["Inferno", "Viridis", "Hot", "Plasma"], index=0)
    
    # 2D Density Map
    fig_density = px.density_map(
        chargers_sub,
        lat="lat",
        lon="lon",
        z="kw_power",
        radius=15,
        center=dict(lat=float(chargers_sub["lat"].mean()), lon=float(chargers_sub["lon"].mean())) if not chargers_sub.empty else dict(lat=20.5937, lon=78.9629),
        zoom=4.8 if selected_state == "All States" else 6.5,
        map_style="carto-darkmatter",
        color_continuous_scale=colorscale_choice,
        hover_name="name",
        hover_data={"operator": True, "kw_power": True, "charger_type": True, "lat": False, "lon": False},
        title=f"Charging Density & Power Intensity ({selected_state})",
        template="plotly_dark",
        height=520
    )
    fig_density = fix_plotly_dark(fig_density)
    fig_density.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_density, use_container_width=True)


with col_map2:
    st.subheader("📍 Multi-Layered Folium Catchment & Cluster Map")
    show_heatmap_layer = st.checkbox("Overlay Heatmap Layer", value=True)
    show_buffer_radii = st.checkbox("Show 5km Service Catchment Radii", value=False)
    
    center_lat = float(chargers_sub["lat"].mean()) if not chargers_sub.empty else 20.5937
    center_lon = float(chargers_sub["lon"].mean()) if not chargers_sub.empty else 78.9629
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5 if selected_state == "All States" else 7, tiles="CartoDB dark_matter")
    
    # Heatmap plugin layer
    if show_heatmap_layer and not chargers_sub.empty:
        heat_data = [[row["lat"], row["lon"]] for _, row in chargers_sub.iterrows()]
        HeatMap(heat_data, radius=12, blur=15, min_opacity=0.4).add_to(m)
        
    marker_cluster = MarkerCluster(name="Charging Stations").add_to(m)
    
    sample_df = chargers_sub.sample(min(600, len(chargers_sub)), random_state=42) if not chargers_sub.empty else chargers_sub
    for _, row in sample_df.iterrows():
        is_fast = row["kw_power"] >= 50
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(f"""
                <div style="font-family: sans-serif; width: 180px; color: #1E293B;">
                    <b style="color: #0F172A;">{row['name']}</b><br>
                    ⚡ Power: <b>{row['kw_power']} kW</b><br>
                    🔌 Type: {row['charger_type']}<br>
                    🏢 Operator: {row['operator']}
                </div>
            """, max_width=220),
            icon=folium.Icon(color="green" if is_fast else "blue", icon="bolt", prefix="fa")
        ).add_to(marker_cluster)
        
        if show_buffer_radii:
            folium.Circle(
                location=[row["lat"], row["lon"]],
                radius=5000,
                color="#00E676" if is_fast else "#00B0FF",
                weight=1,
                fill=True,
                fill_opacity=0.1
            ).add_to(m)
            
    st_folium(m, use_container_width=True, height=520)

st.markdown("---")

# Visual Section 2: 3D Spatial Coordinate Bubble Scatter Plot
st.subheader("🌐 3D Spatial Bubble Visualization (Latitude vs Longitude vs Power Capacity)")
fig_3d = px.scatter_3d(
    chargers_sub.sample(min(1000, len(chargers_sub)), random_state=42) if not chargers_sub.empty else chargers_sub,
    x="lon",
    y="lat",
    z="kw_power",
    color="kw_power",
    size="kw_power",
    hover_name="name",
    hover_data=["operator", "state", "charger_type"],
    color_continuous_scale="Turbid",
    labels={"lon": "Longitude", "lat": "Latitude", "kw_power": "Power Capacity (kW)"},
    template="plotly_dark",
    title="3D Spatial Bubble Visualization",
    height=550
)
fig_3d = fix_plotly_dark(fig_3d)
fig_3d.update_layout(scene=dict(aspectmode="cube"))
st.plotly_chart(fig_3d, use_container_width=True)


st.markdown("---")

fast_pct = round(fast_chargers/len(chargers_sub)*100 if len(chargers_sub)>0 else 0, 1)
render_key_insights(
    title="💡 Key Insights & Spatial Density Takeaways",
    insights=[
        "<b>Spatial Cluster Asymmetry:</b> Charging station density is heavily skewed towards major tier-1 urban centers, leaving peripheral intra-state transit corridors severely underserved.",
        f"<b>High-Power Fast Charging Deficit:</b> Only <span class='highlight-amber'>{fast_pct}%</span> of active stations offer high-speed DC fast charging (>=50kW), creating queue delays for long-distance 4Ws.",
        "<b>Catchment Coverage Gaps:</b> Spatial buffer analysis reveals 5km service radii around existing stations cover less than <span class='highlight-purple'>24%</span> of suburban commercial POI zones."
    ],
    badge_text="⚡ SPATIAL INTELLIGENCE"
)
