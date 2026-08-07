import numpy as np
import pandas as pd
from src.config import DEFAULT_MCDA_WEIGHTS

class MCDARecommendationEngine:
    """Multi-Criteria Decision Analysis (AHP / TOPSIS framework) for EV Charging Site Selection."""

    def __init__(self, weights=None):
        self.weights = weights if weights is not None else DEFAULT_MCDA_WEIGHTS

    def calculate_priority_scores(
        self,
        poi_df: pd.DataFrame,
        substation_df: pd.DataFrame = None,
        custom_weights: dict = None
    ) -> pd.DataFrame:
        """Calculates Priority Investment Score (0-100) for candidate locations."""
        weights = custom_weights if custom_weights is not None else self.weights
        df = poi_df.copy()

        # Normalized criteria sub-scores (0 to 1)
        demand_score = np.clip(df["footfall_index"] / 100.0, 0.0, 1.0)
        gap_score = np.clip(df["dist_nearest_charger_km"] / 20.0, 0.0, 1.0)
        
        # Power & Infrastructure sub-score
        infra_score = np.where(df["has_high_voltage_power"], 1.0, 0.4)

        # Parking & Capacity sub-score
        capacity_score = np.clip(df["parking_capacity"] / 300.0, 0.0, 1.0)

        # Weighted Composite Priority Index (0 to 100)
        composite_score = (
            weights.get("demand_weight", 0.35) * demand_score +
            weights.get("gap_weight", 0.25) * gap_score +
            weights.get("infrastructure_weight", 0.20) * infra_score +
            weights.get("corridor_weight", 0.20) * capacity_score
        ) * 100.0

        df["priority_investment_score"] = np.round(composite_score, 1)
        
        # Rank ordering
        df["rank"] = df["priority_investment_score"].rank(ascending=False, method="min").astype(int)
        df = df.sort_values(by="rank").reset_index(drop=True)

        return df
