import os
import sqlite3
import pandas as pd
from src.config import DB_PATH, DATA_RAW_DIR

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        """Returns SQLite database connection. Ensures DB directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except Exception:
                pass
        return sqlite3.connect(self.db_path)

    def load_raw_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Load dataset from Parquet (fast) or CSV fallback.

        If data files are missing, return an empty DataFrame instead of raising
        so the app can render with graceful degradation.
        """
        parquet_file = os.path.join(DATA_RAW_DIR, f"{dataset_name}.parquet")
        csv_file = os.path.join(DATA_RAW_DIR, f"{dataset_name}.csv")

        try:
            if os.path.exists(parquet_file):
                return pd.read_parquet(parquet_file)
            elif os.path.exists(csv_file):
                return pd.read_csv(csv_file)
            else:
                # Graceful fallback: return empty DataFrame and log warning
                print(f"Warning: dataset {dataset_name} not found in {DATA_RAW_DIR}; returning empty DataFrame.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading dataset {dataset_name}: {e}. Returning empty DataFrame.")
            return pd.DataFrame()

    def sync_parquet_to_sqlite(self):
        """Load all parquet datasets into SQLite tables for SQL queries.

        Errors for individual datasets are logged; the method continues.
        """
        conn = self.get_connection()
        datasets = ["ev_charging_stations", "vahan_ev_registrations", "points_of_interest", "power_substations", "highway_corridors"]
        
        try:
            for name in datasets:
                try:
                    df = self.load_raw_dataset(name)
                    # If empty, skip writing
                    if df is None or df.empty:
                        print(f"Skipping sync for {name}: no data found.")
                        continue
                    df.to_sql(name, conn, if_exists="replace", index=False)
                    print(f"Synced table {name}: {len(df):,} rows into SQLite.")
                except Exception as e:
                    print(f"Error syncing table {name}: {e}")
        finally:
            conn.close()

    def query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query against local SQLite engine."""
        conn = self.get_connection()
        try:
            df = pd.read_sql_query(sql_query, conn)
        finally:
            conn.close()
        return df

db = DatabaseManager()
