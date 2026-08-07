import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

data_raw_dir = r"C:\Users\ADMIN\OneDrive\Desktop\EV\data\raw"

# List of Excel files to convert
excel_files = [
    "ev_charging_stations.xlsx",
    "highway_corridors.xlsx",
    "points_of_interest.xlsx",
    "power_substations.xlsx",
    "vahan_ev_registrations.xlsx"
]

for excel_file in excel_files:
    excel_path = os.path.join(data_raw_dir, excel_file)
    if os.path.exists(excel_path):
        try:
            print(f"Converting {excel_file}...")
            df = pd.read_excel(excel_path)
            
            # Create parquet filename
            parquet_name = excel_file.replace('.xlsx', '.parquet')
            parquet_path = os.path.join(data_raw_dir, parquet_name)
            
            # Save as parquet
            df.to_parquet(parquet_path, index=False)
            print(f"[OK] {parquet_name} created ({len(df):,} rows)")
        except Exception as e:
            print(f"[ERROR] Error converting {excel_file}: {e}")
    else:
        print(f"[SKIP] File not found: {excel_file}")

print("\nConversion complete!")
