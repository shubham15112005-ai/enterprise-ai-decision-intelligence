from pathlib import Path

import pandas as pd


print("Shubham Sharma 23051870")


REQUIRED_COLUMNS = [
    "transaction_date",
    "customer_id",
    "customer_name",
    "product_id",
    "product_name",
    "category",
    "region",
    "quantity",
    "unit_price",
    "revenue",
    "cost",
    "profit",
]


def load_csv(file_path):

    file_path = Path(file_path)

    if not file_path.exists():

        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    df = pd.read_csv(
        file_path
    )

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

    return df


def clean_sales_data(df):

    result = df.copy()

    result = result.drop_duplicates()

    result["transaction_date"] = pd.to_datetime(
        result["transaction_date"],
        errors="coerce"
    )

    numeric_columns = [
        "quantity",
        "unit_price",
        "revenue",
        "cost",
        "profit",
    ]

    for column in numeric_columns:

        result[column] = pd.to_numeric(
            result[column],
            errors="coerce"
        )

    result = result.dropna(
        subset=REQUIRED_COLUMNS
    )

    result["transaction_date"] = (
        result["transaction_date"]
        .dt.strftime("%Y-%m-%d")
    )

    return result.reset_index(
        drop=True
    )