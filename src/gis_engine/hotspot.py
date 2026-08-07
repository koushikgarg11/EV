import numpy as np
import pandas as pd

class ChargingDesertHotspotAnalyzer:
    """Detects high-demand, low-supply spatial cells ('Charging Deserts')."""

    @staticmethod
    def identify_charging_deserts(pois_with_catchment: pd.DataFrame, min_footfall=50, max_chargers_5km=1) -> pd.DataFrame:
        """Flags locations with high commercial footfall index but zero/low charger coverage within 5km."""
        df = pois_with_catchment.copy()

        desert_mask = (
            (df["footfall_index"] >= min_footfall) &
            (df["chargers_within_5km"] <= max_chargers_5km) &
            (df["dist_nearest_charger_km"] >= 4.0)
        )

        df["is_charging_desert"] = desert_mask

        # Desert Severity Score (0 to 100)
        footfall_norm = df["footfall_index"] / 100.0
        dist_norm = np.clip(df["dist_nearest_charger_km"] / 20.0, 0.0, 1.0)
        charger_penalty = np.exp(-0.8 * df["chargers_within_5km"])

        df["desert_severity_index"] = np.where(
            desert_mask,
            np.round((0.5 * footfall_norm + 0.35 * dist_norm + 0.15 * charger_penalty) * 100, 1),
            0.0
        )

        return df
