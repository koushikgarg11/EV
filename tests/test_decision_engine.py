import pandas as pd
from src.decision_engine.mcda import MCDARecommendationEngine
from src.decision_engine.explainability import ExplainableRecommendationEngine

def test_mcda_scoring():
    pois = pd.DataFrame({
        "poi_id": ["P1", "P2"],
        "name": ["Site A", "Site B"],
        "footfall_index": [90, 30],
        "dist_nearest_charger_km": [15.0, 2.0],
        "has_high_voltage_power": [True, False],
        "parking_capacity": [200, 50]
    })
    engine = MCDARecommendationEngine()
    res = engine.calculate_priority_scores(pois)
    assert res.iloc[0]["poi_id"] == "P1", "P1 should rank higher than P2"
    assert res.iloc[0]["priority_investment_score"] > res.iloc[1]["priority_investment_score"]

def test_explainability():
    row = pd.Series({
        "poi_id": "P1",
        "name": "Site A",
        "footfall_index": 90,
        "dist_nearest_charger_km": 15.0,
        "has_high_voltage_power": True,
        "parking_capacity": 200
    })
    explanation = ExplainableRecommendationEngine.explain_recommendation(row, {"demand_weight": 0.35, "gap_weight": 0.25, "infrastructure_weight": 0.20, "corridor_weight": 0.20})
    assert "total_score" in explanation
    assert explanation["confidence_score"] > 80.0
