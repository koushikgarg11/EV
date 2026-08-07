import os
import sqlite3
import pandas as pd
from src.config import DB_PATH, DATA_RAW_DIR

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        """Returns SQLite database connection."""
        return sqlite3.connect(self.db_path)

    def load_raw_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Load dataset from Parquet (fast) or CSV fallback."""
        parquet_file = os.path.join(DATA_RAW_DIR, f"{dataset_name}.parquet")
        csv_file = os.path.join(DATA_RAW_DIR, f"{dataset_name}.csv")

        if os.path.exists(parquet_file):
            return pd.read_parquet(parquet_file)
        elif os.path.exists(csv_file):
            return pd.read_csv(csv_file)
        else:
            raise FileNotFoundError(f"Dataset {dataset_name} not found in {DATA_RAW_DIR}")

    def sync_parquet_to_sqlite(self):
        """Load all 1.3L parquet datasets into SQLite tables for SQL queries."""
        conn = self.get_connection()
        datasets = ["ev_charging_stations", "vahan_ev_registrations", "points_of_interest", "power_substations", "highway_corridors"]
        
        for name in datasets:
            try:
                df = self.load_raw_dataset(name)
                df.to_sql(name, conn, if_exists="replace", index=False)
                print(f"Synced table {name}: {len(df):,} rows into SQLite.")
            except Exception as e:
                print(f"Error syncing table {name}: {e}")
        
        conn.close()

    def query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query against local SQLite engine."""
        conn = self.get_connection()
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df

db = DatabaseManager()
