from typing import Dict, Any


print("Shubham Sharma 23051870")


def calculate_priority(score: float) -> str:

    if score >= 70:
        return "HIGH"

    if score >= 40:
        return "MEDIUM"

    return "LOW"


def customer_risk_recommendation(
    score: float,
    reasons: list[str]
) -> Dict[str, Any]:

    priority = calculate_priority(
        score
    )

    if priority == "HIGH":

        recommendation = (
            "Immediately review the customer account, "
            "pricing, engagement frequency and "
            "profitability. Consider a retention "
            "or account-recovery strategy."
        )

    elif priority == "MEDIUM":

        recommendation = (
            "Review customer engagement and "
            "commercial performance. Consider "
            "targeted offers and account management."
        )

    else:

        recommendation = (
            "Continue monitoring customer performance "
            "and maintain normal account engagement."
        )

    return {
        "decision_type": "CUSTOMER_RISK",
        "priority": priority,
        "score": round(score, 2),
        "recommendation": recommendation,
        "reason": "; ".join(reasons),
    }


def product_opportunity_recommendation(
    score: float
) -> Dict[str, Any]:

    priority = calculate_priority(
        score
    )

    recommendation = (
        "Increase strategic focus on this product. "
        "Evaluate cross-selling, targeted marketing, "
        "sales expansion and customer segmentation."
    )

    return {
        "decision_type": "PRODUCT_OPPORTUNITY",
        "priority": priority,
        "score": round(score, 2),
        "recommendation": recommendation,
        "reason": (
            "Product demonstrates strong commercial "
            "performance and profitability."
        ),
    }


def generic_recommendation(
    decision_type: str,
    score: float,
    reason: str
) -> Dict[str, Any]:

    priority = calculate_priority(
        score
    )

    return {
        "decision_type": decision_type,
        "priority": priority,
        "score": round(score, 2),
        "recommendation": (
            "Review the identified business condition "
            "and take corrective or growth-oriented action."
        ),
        "reason": reason,
    }