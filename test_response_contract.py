import pandas as pd

from models.response import (
    DecisionResponse,
    EvidenceItem,
    RecommendationItem,
    RouteMetadata,
    SourceItem,
)

from services.decision_service import DecisionService


print("Shubham Sharma 23051870")


class FakeOrchestrator:
    """
    Fake orchestrator used to test the service response
    transformation without running the complete pipeline.
    """

    def analyze(self, question, df):

        return {
            "question": question,

            "route": {
                "route": "CUSTOMER_RISK",
                "confidence": 0.85,
                "matched_terms": [
                    "customer",
                    "risk",
                ],
            },

            "kpis": {
                "revenue": 100000.0,
                "profit": 25000.0,
                "transactions": 100,
                "average_order_value": 1000.0,
                "profit_margin": 0.25,
            },

            "customer_insights": [
                {
                    "decision_type": "CUSTOMER_RISK",
                    "entity_type": "customer",
                    "entity_id": "C001",
                    "entity_name": "Customer A",
                    "priority": "HIGH",
                    "score": 82.0,
                    "reason": "Low purchase frequency and margin.",
                    "recommendation": "Launch a retention campaign.",
                    "evidence": [
                        {
                            "source": "Customer Analytics",
                            "metric": "purchase_frequency",
                            "value": 1,
                            "interpretation": (
                                "Customer has low purchase frequency."
                            ),
                            "confidence": 0.90,
                        }
                    ],
                }
            ],

            "product_insights": [
                {
                    "decision_type": "PRODUCT_OPPORTUNITY",
                    "entity_type": "product",
                    "entity_id": "P001",
                    "entity_name": "Product A",
                    "priority": "MEDIUM",
                    "score": 70.0,
                    "reason": "Strong revenue potential.",
                    "recommendation": "Increase product promotion.",
                    "evidence": [],
                }
            ],

            "rag": {
                "context": (
                    "Customer retention policy recommends "
                    "proactive engagement."
                ),

                "sources": [
                    {
                        "title": "Customer Retention Policy",
                        "source": "retention_policy.pdf",
                        "score": 0.91,
                    }
                ],

                "results": [
                    {
                        "title": "Customer Retention Policy",
                        "content": (
                            "Customers with declining activity "
                            "should receive proactive outreach."
                        ),
                        "score": 0.91,
                    }
                ],
            },

            "answer": (
                "Customer A is a high-priority customer risk. "
                "A retention campaign is recommended."
            ),

            "llm_used": False,

            "evidence_available": True,
        }


def sample_dataframe():

    return pd.DataFrame(
        {
            "customer_id": ["C001"],
            "customer_name": ["Customer A"],
            "product_id": ["P001"],
            "product_name": ["Product A"],
            "category": ["Software"],
            "region": ["North"],
            "quantity": [2],
            "unit_price": [500.0],
            "revenue": [1000.0],
            "cost": [500.0],
            "profit": [500.0],
        }
    )


def test_route_metadata():

    route = RouteMetadata(
        route="revenue",
        confidence=0.90,
    )

    assert route.route == "revenue"
    assert route.confidence == 0.90


def test_evidence_item():

    evidence = EvidenceItem(
        source="Analytics",
        metric="revenue",
        value=100000,
        interpretation="Revenue is strong.",
        confidence=0.95,
    )

    assert evidence.source == "Analytics"
    assert evidence.metric == "revenue"
    assert evidence.value == 100000
    assert evidence.confidence == 0.95


def test_recommendation_item():

    recommendation = RecommendationItem(
        decision_type="CUSTOMER_RISK",
        entity_type="customer",
        entity_id="C001",
        entity_name="Customer A",
        priority="HIGH",
        score=82,
        reason="High risk.",
        recommendation="Contact customer.",
    )

    assert recommendation.entity_id == "C001"
    assert recommendation.priority == "HIGH"
    assert recommendation.score == 82


def test_source_item():

    source = SourceItem(
        title="Retention Policy",
        source="policy.pdf",
        score=0.88,
    )

    assert source.title == "Retention Policy"
    assert source.source == "policy.pdf"
    assert source.score == 0.88


def test_decision_response_serialization():

    response = DecisionResponse(
        question="What is our revenue?",
        answer="Revenue is ₹100,000.",
        route=RouteMetadata(
            route="revenue",
            confidence=0.90,
        ),
        kpis={
            "revenue": 100000,
        },
        llm_used=False,
        evidence_available=True,
    )

    data = response.to_dict()

    assert data["question"] == "What is our revenue?"
    assert data["answer"] == "Revenue is ₹100,000."
    assert data["route"]["route"] == "revenue"
    assert data["route"]["confidence"] == 0.90
    assert data["kpis"]["revenue"] == 100000


def test_decision_response_json():

    response = DecisionResponse(
        question="What is our revenue?",
        answer="Revenue is ₹100,000.",
    )

    json_output = response.to_json()

    assert isinstance(json_output, str)
    assert "What is our revenue?" in json_output
    assert "Revenue is" in json_output


def test_service_answer_response():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert isinstance(
        response,
        DecisionResponse,
    )

    assert response.question == (
        "Which customers are at risk?"
    )

    assert response.answer.startswith(
        "Customer A"
    )


def test_service_response_route():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert isinstance(
        response.route,
        RouteMetadata,
    )

    assert response.route.route == (
        "CUSTOMER_RISK"
    )

    assert response.route.confidence == 0.85


def test_service_response_kpis():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert response.kpis["revenue"] == 100000.0
    assert response.kpis["profit"] == 25000.0
    assert response.kpis["transactions"] == 100


def test_service_response_recommendations():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert len(
        response.recommendations
    ) == 2

    first = response.recommendations[0]

    assert first.decision_type == (
        "CUSTOMER_RISK"
    )

    assert first.entity_id == "C001"

    assert first.priority == "HIGH"

    assert first.score == 82.0


def test_service_response_evidence():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert len(
        response.evidence
    ) == 1

    evidence = response.evidence[0]

    assert evidence.source == (
        "Customer Analytics"
    )

    assert evidence.metric == (
        "purchase_frequency"
    )

    assert evidence.value == 1


def test_service_response_sources():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "What does the retention policy recommend?"
    )

    assert len(
        response.sources
    ) == 1

    source = response.sources[0]

    assert source.title == (
        "Customer Retention Policy"
    )

    assert source.source == (
        "retention_policy.pdf"
    )

    assert source.score == 0.91


def test_service_response_rag_context():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "What does the retention policy recommend?"
    )

    assert response.rag_context is not None

    assert "Customer retention policy" in (
        response.rag_context
    )


def test_service_response_metadata():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert response.metadata[
        "rag_result_count"
    ] == 1

    assert response.metadata[
        "customer_insight_count"
    ] == 1

    assert response.metadata[
        "product_insight_count"
    ] == 1


def test_service_response_flags():

    service = DecisionService(
        dataframe=sample_dataframe(),
        orchestrator=FakeOrchestrator(),
    )

    response = service.answer_response(
        "Which customers are at risk?"
    )

    assert response.llm_used is False
    assert response.evidence_available is True