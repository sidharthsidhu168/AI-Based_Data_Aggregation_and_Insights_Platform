import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def run_linear_regression(df: pd.DataFrame, target_col: str, feature_cols: list) -> dict:
    """Train a simple linear regression and return predictions + score."""
    try:
        X = df[feature_cols].select_dtypes(include=[np.number]).dropna()
        y = df[target_col].loc[X.index]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = LinearRegression()
        model.fit(X_train, y_train)

        score = round(model.score(X_test, y_test), 4)
        predictions = model.predict(X_test[:10]).tolist()
        actual = y_test[:10].tolist()

        return {
            "model": "Linear Regression",
            "r2_score": score,
            "predictions": [round(p, 2) for p in predictions],
            "actual": [round(a, 2) for a in actual],
            "coefficients": dict(zip(feature_cols, [round(c, 4) for c in model.coef_]))
        }
    except Exception as e:
        return {"error": str(e)}

def run_clustering(df: pd.DataFrame, n_clusters: int = 3) -> dict:
    """K-Means clustering on numeric columns."""
    try:
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        scaler = StandardScaler()
        scaled = scaler.fit_transform(numeric_df)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(scaled)

        df_result = numeric_df.copy()
        df_result["cluster"] = labels

        cluster_summary = df_result.groupby("cluster").mean().round(2).to_dict()

        return {
            "model": "K-Means Clustering",
            "n_clusters": n_clusters,
            "cluster_sizes": df_result["cluster"].value_counts().to_dict(),
            "cluster_means": cluster_summary
        }
    except Exception as e:
        return {"error": str(e)}

def generate_trend(df: pd.DataFrame, column: str) -> dict:
    """Generate trend data for a numeric column (useful for charts)."""
    if column not in df.columns:
        return {"error": "Column not found"}
    series = df[column].dropna().reset_index(drop=True)
    return {
        "column": column,
        "values": [round(v, 2) for v in series.tolist()[:100]],
        "rolling_mean": [round(v, 2) for v in series.rolling(5).mean().dropna().tolist()[:100]]
    }