from typing import Dict, Any, List

import pandas as pd

from decision_engine.evidence import (
    build_evidence,
)

from decision_engine.recommendation import (
    customer_risk_recommendation,
    product_opportunity_recommendation,
)


print("Shubham Sharma 23051870")


def generate_customer_insights(
    customer_df: pd.DataFrame
) -> List[Dict[str, Any]]:

    if customer_df.empty:
        return []

    insights = []

    average_revenue = (
        customer_df["revenue"].mean()
    )

    average_transactions = (
        customer_df["transactions"].mean()
    )

    average_margin = (
        customer_df["profit_margin"].mean()
    )

    for _, row in customer_df.iterrows():

        score = 0
        reasons = []
        evidence = []

        # ---------------------------------------------
        # Profitability
        # ---------------------------------------------

        if row["profit_margin"] < 0.20:

            score += 35

            reasons.append(
                "Customer has a low profit margin."
            )

            evidence.append(
                build_evidence(
                    source="Customer Analytics",
                    metric="Profit Margin",
                    value=f"{row['profit_margin']:.2%}",
                    interpretation=(
                        "Profitability is below the "
                        "healthy business threshold."
                    ),
                )
            )

        # ---------------------------------------------
        # Revenue
        # ---------------------------------------------

        if row["revenue"] < average_revenue:

            score += 20

            reasons.append(
                "Customer revenue is below portfolio average."
            )

            evidence.append(
                build_evidence(
                    source="Customer Analytics",
                    metric="Revenue",
                    value=f"{row['revenue']:,.2f}",
                    interpretation=(
                        "Revenue is below the average "
                        "customer revenue."
                    ),
                )
            )

        # ---------------------------------------------
        # Transactions
        # ---------------------------------------------

        if (
            row["transactions"]
            < average_transactions
        ):

            score += 20

            reasons.append(
                "Customer transaction frequency is low."
            )

            evidence.append(
                build_evidence(
                    source="Customer Analytics",
                    metric="Transactions",
                    value=int(row["transactions"]),
                    interpretation=(
                        "Transaction activity is below "
                        "the customer portfolio average."
                    ),
                )
            )

        # ---------------------------------------------
        # Margin compared with portfolio
        # ---------------------------------------------

        if (
            row["profit_margin"]
            < average_margin
        ):

            score += 15

            reasons.append(
                "Customer margin is below portfolio average."
            )

        if score < 35:
            continue

        recommendation = (
            customer_risk_recommendation(
                score,
                reasons
            )
        )

        insights.append({
            "decision_type":
                recommendation["decision_type"],

            "entity_type":
                "CUSTOMER",

            "entity_id":
                row["customer_id"],

            "entity_name":
                row["customer_name"],

            "priority":
                recommendation["priority"],

            "score":
                recommendation["score"],

            "reason":
                recommendation["reason"],

            "recommendation":
                recommendation["recommendation"],

            "evidence":
                evidence,
        })

    return insights


def generate_product_insights(
    df: pd.DataFrame
) -> List[Dict[str, Any]]:

    if df.empty:
        return []

    product_df = (
        df.groupby(
            [
                "product_id",
                "product_name",
                "category",
            ]
        )
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            quantity=("quantity", "sum"),
        )
        .reset_index()
    )

    product_df["profit_margin"] = (
        product_df["profit"]
        / product_df["revenue"]
    )

    revenue_threshold = (
        product_df["revenue"]
        .quantile(0.75)
    )

    margin_threshold = (
        product_df["profit_margin"]
        .quantile(0.75)
    )

    insights = []

    for _, row in product_df.iterrows():

        if (
            row["revenue"] >= revenue_threshold
            and
            row["profit_margin"]
            >= margin_threshold
        ):

            evidence = [
                build_evidence(
                    source="Product Analytics",
                    metric="Revenue",
                    value=f"{row['revenue']:,.2f}",
                    interpretation=(
                        "Product revenue is in the "
                        "top performance quartile."
                    ),
                ),
                build_evidence(
                    source="Product Analytics",
                    metric="Profit Margin",
                    value=f"{row['profit_margin']:.2%}",
                    interpretation=(
                        "Product profitability is in "
                        "the top performance quartile."
                    ),
                ),
            ]

            recommendation = (
                product_opportunity_recommendation(
                    90
                )
            )

            insights.append({
                "decision_type":
                    recommendation["decision_type"],

                "entity_type":
                    "PRODUCT",

                "entity_id":
                    row["product_id"],

                "entity_name":
                    row["product_name"],

                "priority":
                    recommendation["priority"],

                "score":
                    recommendation["score"],

                "reason":
                    recommendation["reason"],

                "recommendation":
                    recommendation["recommendation"],

                "evidence":
                    evidence,
            })

    return insights