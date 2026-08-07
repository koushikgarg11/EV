import numpy as np
import pandas as pd

class NetworkCorridorAnalyzer:
    """Analyzes National Highway corridors, inter-city connectivity, and corridor distance decay gaps."""

    @staticmethod
    def analyze_corridor_readiness(highway_df: pd.DataFrame, charger_df: pd.DataFrame) -> pd.DataFrame:
        """Evaluates highway corridor readiness index along NH routes."""
        df = highway_df.copy()

        # Compute Corridor Accessibility Score (0-100)
        # Higher score = High traffic + long distance to nearest charger (High urgency for investment)
        dist_factor = np.clip(df["nearest_charger_dist_km"] / 35.0, 0.0, 1.0)
        traffic_factor = np.clip(df["daily_traffic_volume"] / 75000.0, 0.0, 1.0)
        freight_factor = np.clip(df["freight_percentage"] / 40.0, 0.0, 1.0)

        df["corridor_gap_score"] = np.round((0.5 * dist_factor + 0.35 * traffic_factor + 0.15 * freight_factor) * 100, 1)

        # Readiness classification
        conditions = [
            (df["nearest_charger_dist_km"] <= 10.0),
            (df["nearest_charger_dist_km"] <= 25.0),
            (df["nearest_charger_dist_km"] > 25.0)
        ]
        choices = ["High Readiness (Well Served)", "Moderate Gap", "Critical Charging Desert"]
        df["readiness_status"] = np.select(conditions, choices, default="Moderate Gap")

        return df
