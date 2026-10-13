import pandas as pd


print("Shubham Sharma 23051870")


def calculate_kpis(df: pd.DataFrame):

    if df.empty:

        return {
            "revenue": 0.0,
            "profit": 0.0,
            "transactions": 0,
            "average_order_value": 0.0,
            "profit_margin": 0.0,
        }

    revenue = float(
        df["revenue"].sum()
    )

    profit = float(
        df["profit"].sum()
    )

    transactions = int(
        len(df)
    )

    average_order_value = (
        revenue / transactions
        if transactions
        else 0
    )

    profit_margin = (
        profit / revenue
        if revenue
        else 0
    )

    return {
        "revenue": revenue,
        "profit": profit,
        "transactions": transactions,
        "average_order_value": average_order_value,
        "profit_margin": profit_margin,
    }


def calculate_customer_metrics(df):

    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby(
            [
                "customer_id",
                "customer_name"
            ]
        )
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            transactions=("revenue", "count"),
            quantity=("quantity", "sum"),
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["profit"]
        / result["revenue"]
    )

    return result


def calculate_product_metrics(df):

    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby(
            [
                "product_id",
                "product_name",
                "category"
            ]
        )
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            quantity=("quantity", "sum"),
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["profit"]
        / result["revenue"]
    )

    return result