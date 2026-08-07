import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SQL_DIR = os.path.join(BASE_DIR, "sql")
DB_PATH = os.path.join(BASE_DIR, "ev_platform.db")

# Coordinate Reference Systems
WGS84_CRS = "EPSG:4326"        # Geographic WGS84 (Lat/Lon)
INDIAN_GRID_CRS = "EPSG:7755"  # Indian National Grid projected CRS (meters)

# Default MCDA Weights for Recommendation Engine
DEFAULT_MCDA_WEIGHTS = {
    "demand_weight": 0.35,          # EV registrations, vehicle density, POI footfall
    "gap_weight": 0.25,             # Distance to nearest existing charging station
    "corridor_weight": 0.20,        # Proximity to National Highways & daily traffic volume
    "infrastructure_weight": 0.15,  # Power substation capacity & voltage availability
    "growth_weight": 0.05           # YoY EV adoption growth rate
}

# H3 / Hex Grid Spatial Resolution Settings
HEX_RESOLUTION = 7  # Approx 5.16 sq km hex grid cell area
