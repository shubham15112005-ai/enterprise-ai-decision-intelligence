import pandas as pd

from decision_engine.evidence import (
    build_evidence,
    combine_evidence,
)

from decision_engine.recommendation import (
    calculate_priority,
    customer_risk_recommendation,
)

from decision_engine.query_router import (
    route_query,
)

from decision_engine.insight_generator import (
    generate_customer_insights,
)


print("Shubham Sharma 23051870")


def test_priority():

    assert calculate_priority(80) == "HIGH"

    assert calculate_priority(50) == "MEDIUM"

    assert calculate_priority(20) == "LOW"


def test_evidence():

    evidence = build_evidence(
        source="Analytics",
        metric="Revenue",
        value=10000,
        interpretation="Strong revenue performance",
    )

    assert evidence["source"] == "Analytics"
    assert evidence["metric"] == "Revenue"
    assert evidence["value"] == 10000


def test_combine_evidence():

    items = [
        build_evidence(
            "Analytics",
            "Revenue",
            1000,
            "Good"
        ),

        build_evidence(
            "Analytics",
            "Profit",
            500,
            "Strong"
        ),
    ]

    result = combine_evidence(
        items
    )

    assert "Revenue" in result
    assert "Profit" in result


def test_customer_recommendation():

    result = customer_risk_recommendation(
        80,
        [
            "Low margin",
            "Low transaction frequency",
        ],
    )

    assert result["priority"] == "HIGH"
    assert result["decision_type"] == (
        "CUSTOMER_RISK"
    )


def test_query_router():

    result = route_query(
        "Which customers are at risk?"
    )

    assert result["route"] in {
        "customer",
        "risk",
    }

    result = route_query(
        "What is our total revenue?"
    )

    assert result["route"] == "revenue"


def test_customer_insight_generation():

    df = pd.DataFrame({

        "customer_id": [
            "C001",
            "C002",
            "C003",
        ],

        "customer_name": [
            "Alpha",
            "Beta",
            "Gamma",
        ],

        "revenue": [
            1000,
            10000,
            500,
        ],

        "profit": [
            100,
            5000,
            50,
        ],

        "transactions": [
            1,
            20,
            1,
        ],

        "quantity": [
            5,
            50,
            2,
        ],

        "profit_margin": [
            0.10,
            0.50,
            0.10,
        ],
    })

    results = generate_customer_insights(
        df
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) > 0