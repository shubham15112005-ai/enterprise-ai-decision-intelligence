import pandas as pd

from analytics.metrics import (
    calculate_kpis,
    calculate_customer_metrics,
    calculate_product_metrics,
)

from analytics.statistics import (
    monthly_revenue,
    detect_revenue_anomalies,
)


print("Shubham Sharma 23051870")


def sample_dataframe():

    return pd.DataFrame({
        "transaction_date": [
            "2026-01-01",
            "2026-01-15",
            "2026-02-01",
        ],

        "customer_id": [
            "C001",
            "C001",
            "C002",
        ],

        "customer_name": [
            "Customer A",
            "Customer A",
            "Customer B",
        ],

        "product_id": [
            "P001",
            "P002",
            "P001",
        ],

        "product_name": [
            "Product A",
            "Product B",
            "Product A",
        ],

        "category": [
            "Software",
            "AI",
            "Software",
        ],

        "region": [
            "North",
            "North",
            "South",
        ],

        "quantity": [
            2,
            1,
            3,
        ],

        "unit_price": [
            100,
            200,
            100,
        ],

        "revenue": [
            200,
            200,
            300,
        ],

        "cost": [
            100,
            100,
            150,
        ],

        "profit": [
            100,
            100,
            150,
        ],
    })


def test_kpis():

    df = sample_dataframe()

    kpis = calculate_kpis(df)

    assert kpis["revenue"] == 700
    assert kpis["profit"] == 350
    assert kpis["transactions"] == 3


def test_customer_metrics():

    df = sample_dataframe()

    result = calculate_customer_metrics(
        df
    )

    assert len(result) == 2

    customer_a = result[
        result["customer_id"] == "C001"
    ].iloc[0]

    assert customer_a["revenue"] == 400


def test_product_metrics():

    df = sample_dataframe()

    result = calculate_product_metrics(
        df
    )

    assert len(result) == 2


def test_monthly_revenue():

    df = sample_dataframe()

    result = monthly_revenue(
        df
    )

    assert len(result) == 2


def test_anomaly_detection():

    df = sample_dataframe()

    result = detect_revenue_anomalies(
        df
    )

    assert "anomaly_score" in result.columns
    assert "is_anomaly" in result.columns