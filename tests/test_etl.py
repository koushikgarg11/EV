import pandas as pd
from src.etl.cleaner import DataCleaner

def test_validate_coordinates():
    df = pd.DataFrame({
        "lat": [19.0760, 0.0, 99.0, 28.6139],
        "lon": [72.8777, 0.0, -10.0, 77.2090]
    })
    cleaned = DataCleaner.validate_coordinates(df)
    assert len(cleaned) == 2, f"Expected 2 valid coordinate rows, got {len(cleaned)}"

def test_missing_values():
    df = pd.DataFrame({
        "category": ["Mall", None, "Tech Park"],
        "val": [10.0, None, 30.0]
    })
    cleaned = DataCleaner.handle_missing_values(df)
    assert cleaned["category"].isnull().sum() == 0
    assert cleaned["val"].isnull().sum() == 0
