from typing import Dict


print("Shubham Sharma 23051870")


ROUTES = {
    "revenue": [
        "revenue",
        "sales",
        "income",
        "turnover",
    ],

    "profit": [
        "profit",
        "margin",
        "profitable",
        "profitability",
    ],

    "customer": [
        "customer",
        "client",
        "account",
        "retention",
    ],

    "product": [
        "product",
        "item",
        "offering",
        "sku",
    ],

    "region": [
        "region",
        "geography",
        "location",
        "area",
    ],

    "risk": [
        "risk",
        "danger",
        "problem",
        "threat",
    ],

    "recommendation": [
        "recommend",
        "recommendation",
        "should",
        "action",
        "what should",
    ],

    "knowledge": [
        "policy",
        "document",
        "procedure",
        "guideline",
        "regulation",
    ],
}


def route_query(
    query: str
) -> Dict[str, object]:

    query = query.lower().strip()

    scores = {
        route: 0
        for route in ROUTES
    }

    matched_terms = {
        route: []
        for route in ROUTES
    }

    for route, keywords in ROUTES.items():

        for keyword in keywords:

            if keyword in query:

                scores[route] += 1

                matched_terms[
                    route
                ].append(keyword)

    best_route = max(
        scores,
        key=scores.get
    )

    best_score = scores[
        best_route
    ]

    if best_score == 0:

        best_route = "general"

    return {
        "route": best_route,
        "confidence": (
            min(
                best_score / 3,
                1.0
            )
            if best_score
            else 0.0
        ),
        "matched_terms":
            matched_terms.get(
                best_route,
                []
            ),
    }