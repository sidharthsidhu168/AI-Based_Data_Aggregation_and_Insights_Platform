import pandas as pd
import numpy as np

def load_and_clean(file_path: str) -> pd.DataFrame:
    """Load a CSV or Excel and auto-clean it."""
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Drop completely empty rows/columns
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # Fill numeric nulls with column median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill text nulls with 'Unknown'
    text_cols = df.select_dtypes(include=["object"]).columns
    df[text_cols] = df[text_cols].fillna("Unknown")

    return df

def get_summary_stats(df: pd.DataFrame) -> dict:
    """Return basic statistics for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    stats = {}
    for col in numeric_df.columns:
        stats[col] = {
            "mean": round(float(numeric_df[col].mean()), 2),
            "median": round(float(numeric_df[col].median()), 2),
            "std": round(float(numeric_df[col].std()), 2),
            "min": round(float(numeric_df[col].min()), 2),
            "max": round(float(numeric_df[col].max()), 2),
        }
    return stats

def detect_anomalies(df: pd.DataFrame, column: str) -> list:
    """Use IQR method to detect outliers/anomalies."""
    if column not in df.columns:
        return []
    series = df[column].dropna()
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    anomalies = df[(df[column] < lower) | (df[column] > upper)]
    return anomalies.head(20).to_dict(orient="records")