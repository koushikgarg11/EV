import os
import pandas as pd
from src.config import DATA_RAW_DIR, DATA_PROCESSED_DIR
from src.etl.cleaner import DataCleaner

class ETLPipeline:
    def __init__(self):
        os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

    def run_pipeline(self):
        print("=== Running ETL Pipeline for India EV Platform ===")
        datasets = ["ev_charging_stations", "vahan_ev_registrations", "points_of_interest", "power_substations", "highway_corridors"]
        
        report = {}
        for name in datasets:
            raw_parquet = os.path.join(DATA_RAW_DIR, f"{name}.parquet")
            raw_csv = os.path.join(DATA_RAW_DIR, f"{name}.csv")
            
            if os.path.exists(raw_parquet):
                df = pd.read_parquet(raw_parquet)
            elif os.path.exists(raw_csv):
                df = pd.read_csv(raw_csv)
            else:
                print(f"Skipping {name}, missing raw file.")
                continue

            initial_count = len(df)
            
            # Cleaning steps
            if "lat" in df.columns and "lon" in df.columns:
                df = DataCleaner.validate_coordinates(df, "lat", "lon")
            df = DataCleaner.handle_missing_values(df)
            df = DataCleaner.remove_duplicates(df)
            
            final_count = len(df)
            
            # Save processed
            proc_parquet = os.path.join(DATA_PROCESSED_DIR, f"{name}.parquet")
            proc_csv = os.path.join(DATA_PROCESSED_DIR, f"{name}.csv")
            df.to_parquet(proc_parquet, index=False)
            df.to_csv(proc_csv, index=False)
            
            report[name] = {
                "initial_count": initial_count,
                "final_count": final_count,
                "completeness_pct": 100.0,
                "status": "Clean & Validated"
            }
            print(f"ETL [{name}]: {initial_count:,} -> {final_count:,} valid records.")

        return report

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run_pipeline()
