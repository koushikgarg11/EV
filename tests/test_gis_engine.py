import pandas as pd
from src.gis_engine.spatial_index import SpatialIndexEngine
from src.gis_engine.catchment import CatchmentAnalyzer

def test_kdtree_spatial_index():
    chargers = pd.DataFrame({
        "lat": [19.0760, 28.6139],
        "lon": [72.8777, 77.2090]
    })
    tree, coords = SpatialIndexEngine.build_kdtree(chargers)
    
    query = pd.DataFrame({
        "lat": [19.0800],
        "lon": [72.8800]
    })
    dist_km, indices = SpatialIndexEngine.query_nearest_neighbors(tree, query)
    assert dist_km[0] < 5.0, f"Expected distance < 5km, got {dist_km[0]}"
    assert indices[0] == 0

def test_catchment_coverage():
    chargers = pd.DataFrame({
        "lat": [19.0760],
        "lon": [72.8777]
    })
    pois = pd.DataFrame({
        "poi_id": ["P1"],
        "lat": [19.0770],
        "lon": [72.8780]
    })
    res = CatchmentAnalyzer.calculate_catchment_coverage(pois, chargers)
    assert res["chargers_within_2km"].iloc[0] == 1
