import pandas as pd
import numpy as np


print("Shubham Sharma 23051870")


def revenue_statistics(df):

    if df.empty:
        return {}

    revenue = df["revenue"]

    return {
        "mean": float(revenue.mean()),
        "median": float(revenue.median()),
        "std": float(revenue.std()),
        "minimum": float(revenue.min()),
        "maximum": float(revenue.max()),
    }


def detect_revenue_anomalies(
    df,
    z_threshold=2.5
):

    if df.empty:
        return df.copy()

    result = df.copy()

    mean = result["revenue"].mean()

    std = result["revenue"].std()

    if std == 0 or pd.isna(std):

        result["anomaly_score"] = 0.0
        result["is_anomaly"] = False

        return result

    result["anomaly_score"] = (
        (result["revenue"] - mean)
        / std
    )

    result["is_anomaly"] = (
        result["anomaly_score"].abs()
        >= z_threshold
    )

    return result


def monthly_revenue(df):

    if df.empty:
        return pd.DataFrame()

    result = df.copy()

    result["transaction_date"] = pd.to_datetime(
        result["transaction_date"]
    )

    result["month"] = (
        result["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    return (
        result.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
        )
        .reset_index()
    )