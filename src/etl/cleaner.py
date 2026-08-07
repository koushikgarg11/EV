import numpy as np
import pandas as pd

class DataCleaner:
    @staticmethod
    def validate_coordinates(df: pd.DataFrame, lat_col="lat", lon_col="lon") -> pd.DataFrame:
        """Filters out invalid coordinates outside India boundary box (Lat 6.0 to 38.0, Lon 68.0 to 98.0)."""
        initial_len = len(df)
        valid_mask = (
            (df[lat_col] >= 6.0) & (df[lat_col] <= 38.0) &
            (df[lon_col] >= 68.0) & (df[lon_col] <= 98.0) &
            (df[lat_col].notnull()) & (df[lon_col].notnull())
        )
        cleaned_df = df[valid_mask].copy()
        dropped = initial_len - len(cleaned_df)
        if dropped > 0:
            print(f"Coordinate validation: Dropped {dropped} invalid coordinate rows.")
        return cleaned_df

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """Fills missing categoricals and numericals with safe defaults."""
        cleaned_df = df.copy()
        for col in cleaned_df.columns:
            if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                median_val = cleaned_df[col].median()
                cleaned_df[col] = cleaned_df[col].fillna(median_val if pd.notnull(median_val) else 0)
            else:
                cleaned_df[col] = cleaned_df[col].fillna("Unknown")
        return cleaned_df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset_cols=None) -> pd.DataFrame:
        """Deduplicates dataframe rows."""
        initial_len = len(df)
        cleaned_df = df.drop_duplicates(subset=subset_cols)
        dropped = initial_len - len(cleaned_df)
        if dropped > 0:
            print(f"Deduplication: Dropped {dropped} duplicate rows.")
        return cleaned_df
