import pandas as pd
from src.decision_engine.mcda import MCDARecommendationEngine

class ScenarioSimulatorEngine:
    """What-If scenario simulator engine for dynamic weight tuning and budget allocation."""

    @staticmethod
    def run_simulation(poi_df: pd.DataFrame, custom_weights: dict, top_n=20) -> pd.DataFrame:
        """Simulates candidate rankings under custom user-selected weights."""
        mcda = MCDARecommendationEngine()
        ranked_df = mcda.calculate_priority_scores(poi_df, custom_weights=custom_weights)
        return ranked_df.head(top_n)
