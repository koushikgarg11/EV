# System Architecture Specification

```
                          +---------------------------------------+
                          |   1.3 Lakh Geospatial Datasets       |
                          | (OSM, Vahan, POI, Highways, Grid)     |
                          +-------------------+-------------------+
                                              |
                                              v
                          +---------------------------------------+
                          |      Data Engineering & ETL           |
                          | (Cleaner, Bounds Validation, Parquet) |
                          +-------------------+-------------------+
                                              |
                                              v
                          +---------------------------------------+
                          |      GIS Analytics Engine             |
                          | (SciPy KDTree, H3 Grid, Catchments)   |
                          +-------------------+-------------------+
                                              |
                                              v
                          +---------------------------------------+
                          |      Decision Intelligence Engine     |
                          | (AHP MCDA Scoring, SHAP Explainability)|
                          +-------------------+-------------------+
                                              |
                                              v
                          +---------------------------------------+
                          |  Streamlit Multi-Page Dashboard       |
                          | (PyDeck 3D Hexagon, Folium, Slider UI)|
                          +---------------------------------------+
```
