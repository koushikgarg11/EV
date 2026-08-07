import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from src.database.db_manager import db

st.set_page_config(page_title="Spatial Infrastructure", page_icon="🗺️", layout="wide")

st.title("🗺️ Spatial Infrastructure & Density Analytics")
st.markdown("### *PyDeck 3D Hexagon density layers and interactive charging station cluster maps across India.*")
st.markdown("---")

df_chargers = db.load_raw_dataset("ev_charging_stations")
df_pois = db.load_raw_dataset("points_of_interest")

st.sidebar.header("Filter Region")
selected_state = st.sidebar.selectbox("Select State", ["All States"] + list(df_chargers["state"].unique()))

if selected_state != "All States":
    chargers_sub = df_chargers[df_chargers["state"] == selected_state]
    pois_sub = df_pois[df_pois["state"] == selected_state]
else:
    chargers_sub = df_chargers
    pois_sub = df_pois

col_map1, col_map2 = st.columns(2)

with col_map1:
    st.subheader("🔥 PyDeck 3D Hexagon Density Map")
    
    # 3D Hexagon Layer
    hex_layer = pdk.Layer(
        "HexagonLayer",
        data=chargers_sub[["lat", "lon"]],
        get_position=["lon", "lat"],
        radius=12000,
        elevation_scale=150,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=0.9,
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=float(chargers_sub["lat"].mean()),
        longitude=float(chargers_sub["lon"].mean()),
        zoom=5.5,
        pitch=45,
    )
    
    r = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view_state,
        tooltip={"text": "Chargers Count: {elevationValue}"},
        map_style="mapbox://styles/mapbox/dark-v10"
    )
    st.pydeck_chart(r)

with col_map2:
    st.subheader("📍 Clustered Charging Station Map (Folium)")
    
    center_lat = float(chargers_sub["lat"].mean())
    center_lon = float(chargers_sub["lon"].mean())
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles="CartoDB dark_matter")
    marker_cluster = MarkerCluster().add_to(m)
    
    # Sample top 800 for fast rendering in Folium map
    sample_df = chargers_sub.sample(min(800, len(chargers_sub)), random_state=42)
    for _, row in sample_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>{row['name']}</b><br>Operator: {row['operator']}<br>Power: {row['kw_power']} kW<br>Type: {row['charger_type']}",
            icon=folium.Icon(color="green" if row["kw_power"] >= 50 else "blue", icon="bolt", prefix="fa")
        ).add_to(marker_cluster)
        
    st_folium(m, width=650, height=450)
