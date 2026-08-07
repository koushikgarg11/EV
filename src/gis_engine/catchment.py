import numpy as np
import pandas as pd
from scipy.spatial import KDTree

class CatchmentAnalyzer:
    """Analyzes spatial catchment areas and charging station coverage radii (2km, 5km, 10km)."""

    @staticmethod
    def calculate_catchment_coverage(poi_df: pd.DataFrame, charger_df: pd.DataFrame) -> pd.DataFrame:
        """Calculates distance from each POI/grid cell to nearest charging station and counts chargers within radii."""
        charger_coords = np.column_stack((charger_df["lat"].values, charger_df["lon"].values))
        tree = KDTree(charger_coords)

        poi_coords = np.column_stack((poi_df["lat"].values, poi_df["lon"].values))
        distances, indices = tree.query(poi_coords, k=1)
        dist_km = distances * 111.0

        # Count chargers within 2km, 5km, 10km
        count_2km = tree.query_ball_point(poi_coords, r=2.0 / 111.0)
        count_5km = tree.query_ball_point(poi_coords, r=5.0 / 111.0)
        count_10km = tree.query_ball_point(poi_coords, r=10.0 / 111.0)

        result_df = poi_df.copy()
        result_df["dist_nearest_charger_km"] = np.round(dist_km, 2)
        result_df["chargers_within_2km"] = [len(c) for c in count_2km]
        result_df["chargers_within_5km"] = [len(c) for c in count_5km]
        result_df["chargers_within_10km"] = [len(c) for c in count_10km]

        return result_df
