import numpy as np
import pandas as pd
from scipy.spatial import KDTree

class SpatialIndexEngine:
    """High-performance Spatial Indexing Engine using KDTree for 1.3L record spatial searches."""
    
    @staticmethod
    def build_kdtree(df: pd.DataFrame, lat_col="lat", lon_col="lon"):
        """Build SciPy KDTree from spatial coordinates (converted to approx km projection)."""
        coords = np.column_stack((df[lat_col].values, df[lon_col].values))
        tree = KDTree(coords)
        return tree, coords

    @staticmethod
    def query_nearest_neighbors(tree: KDTree, query_df: pd.DataFrame, lat_col="lat", lon_col="lon", k=1):
        """Query nearest neighbor distance (in degrees & converted approx km) for query coordinates."""
        query_coords = np.column_stack((query_df[lat_col].values, query_df[lon_col].values))
        distances, indices = tree.query(query_coords, k=k)
        
        # Approximate degree to km conversion in India (1 degree lat ~ 111km)
        dist_km = distances * 111.0
        return np.round(dist_km, 2), indices

    @staticmethod
    def generate_spatial_hex_grid(df: pd.DataFrame, grid_step=0.08, lat_col="lat", lon_col="lon"):
        """Generates regular spatial grid (hex-like cells) across dataset bounding box."""
        min_lat, max_lat = df[lat_col].min(), df[lat_col].max()
        min_lon, max_lon = df[lon_col].min(), df[lon_col].max()

        lat_grid = np.arange(min_lat, max_lat, grid_step)
        lon_grid = np.arange(min_lon, max_lon, grid_step)

        grid_cells = []
        cell_id = 1
        for lat in lat_grid:
            for lon in lon_grid:
                grid_cells.append({
                    "hex_id": f"HEX_IN_{cell_id:06d}",
                    "lat": round(lat + grid_step / 2, 5),
                    "lon": round(lon + grid_step / 2, 5),
                    "min_lat": round(lat, 5),
                    "max_lat": round(lat + grid_step, 5),
                    "min_lon": round(lon, 5),
                    "max_lon": round(lon + grid_step, 5)
                })
                cell_id += 1

        return pd.DataFrame(grid_cells)
