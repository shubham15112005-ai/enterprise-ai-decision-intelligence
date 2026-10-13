import random
from datetime import datetime, timedelta

import pandas as pd

from config.settings import RAW_DATA_DIR


print("Shubham Sharma 23051870")


CUSTOMERS = [
    ("C001", "Acme Corporation"),
    ("C002", "Global Industries"),
    ("C003", "TechNova Solutions"),
    ("C004", "Future Systems"),
    ("C005", "Prime Retail"),
    ("C006", "Vertex Technologies"),
    ("C007", "BlueSky Enterprises"),
    ("C008", "NextGen Solutions"),
    ("C009", "Alpha Manufacturing"),
    ("C010", "Zenith Corp"),
]


PRODUCTS = [
    ("P001", "Enterprise Cloud Suite", "Software", 1200),
    ("P002", "Analytics Platform", "Software", 950),
    ("P003", "AI Assistant", "AI", 1500),
    ("P004", "Data Integration Suite", "Data", 1100),
    ("P005", "Cybersecurity Platform", "Security", 1800),
    ("P006", "CRM Enterprise", "Business", 1300),
    ("P007", "Supply Chain Optimizer", "Operations", 1650),
    ("P008", "Business Intelligence Pro", "Analytics", 1000),
]


REGIONS = [
    "North",
    "South",
    "East",
    "West",
]


def generate_data(
    number_of_records=1500
):

    random.seed(42)

    records = []

    start_date = (
        datetime.now()
        - timedelta(days=365)
    )

    for _ in range(
        number_of_records
    ):

        customer_id, customer_name = (
            random.choice(CUSTOMERS)
        )

        (
            product_id,
            product_name,
            category,
            base_price,
        ) = random.choice(
            PRODUCTS
        )

        region = random.choice(
            REGIONS
        )

        quantity = random.randint(
            1,
            20
        )

        unit_price = round(
            base_price
            * random.uniform(
                0.85,
                1.15
            ),
            2
        )

        revenue = round(
            quantity * unit_price,
            2
        )

        cost = round(
            revenue
            * random.uniform(
                0.45,
                0.80
            ),
            2
        )

        profit = round(
            revenue - cost,
            2
        )

        date = (
            start_date
            + timedelta(
                days=random.randint(
                    0,
                    365
                )
            )
        )

        records.append({
            "transaction_date":
                date.strftime("%Y-%m-%d"),
            "customer_id":
                customer_id,
            "customer_name":
                customer_name,
            "product_id":
                product_id,
            "product_name":
                product_name,
            "category":
                category,
            "region":
                region,
            "quantity":
                quantity,
            "unit_price":
                unit_price,
            "revenue":
                revenue,
            "cost":
                cost,
            "profit":
                profit,
        })

    df = pd.DataFrame(
        records
    )

    output = (
        RAW_DATA_DIR
        / "sales_transactions.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    print(
        f"Generated {len(df)} transactions."
    )

    print(
        f"File: {output}"
    )


if __name__ == "__main__":
    generate_data()