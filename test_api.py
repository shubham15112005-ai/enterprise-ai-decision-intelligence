from urllib import response

from fastapi.testclient import TestClient
from plotly import data

from api_app import app
from api import routes
from models.response import DecisionResponse


print("Shubham Sharma 23051870")


class FakeService:
    """
    Lightweight fake service for API tests.

    This prevents the tests from depending on:
    - database state
    - LLM API
    - RAG documents
    - external services
    """

    def health_check(self):
        return {
            "status": "healthy",
            "service": "DecisionService",
        }

    def answer_response(self, question):
        return DecisionResponse(
            question=question,
            answer="Test decision response.",
            route={
                "route": "revenue",
                "confidence": 0.8,
            },
            kpis={
                "revenue": 100000,
                "profit": 20000,
            },
            customer_insights=[],
            product_insights=[],
            evidence=[],
            recommendations=[],
            sources=[],
            rag_context="",
            llm_used=False,
            evidence_available=True,
            metadata={
                "test": True,
            },
        )


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == (
        "Enterprise AI Decision Intelligence"
    )

    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_health_endpoint(monkeypatch):
    monkeypatch.setattr(
        routes,
        "_service",
        FakeService(),
    )

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "DecisionService"


def test_ask_endpoint(monkeypatch):
    monkeypatch.setattr(
        routes,
        "_service",
        FakeService(),
    )

    response = client.post(
        "/api/ask",
        json={
            "question": "What is our revenue?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == (
        "What is our revenue?"
    )

    assert data["answer"] == (
        "Test decision response."
    )

    assert data["route"]["route"] == "revenue"

    assert data["route"]["confidence"] == 0.8


def test_ask_endpoint_requires_question():
    response = client.post(
        "/api/ask",
        json={},
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == (
        "VALIDATION_ERROR"
    )

    assert data["error"]["status"] == 422

    assert "question" in (
        data["error"]["message"]
    )


def test_ask_endpoint_rejects_empty_question():
    response = client.post(
        "/api/ask",
        json={
            "question": ""
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == (
        "VALIDATION_ERROR"
    )

    assert data["error"]["status"] == 422

def test_ask_endpoint_handles_service_error(
    monkeypatch,
):
    class ErrorService:
        def answer_response(self, question):
            raise ValueError(
                "Question cannot be processed."
            )

    monkeypatch.setattr(
        routes,
        "_service",
        ErrorService(),
    )

    response = client.post(
        "/api/ask",
        json={
            "question": "test"
        },
    )

    assert response.status_code == 400

    error_payload = response.json()

    assert error_payload["error"]["code"] == (
        "INVALID_QUESTION"
    )

    assert error_payload["error"]["message"] == (
        "Question cannot be processed."
    )

    assert error_payload["error"]["status"] == 400

def test_cors_headers():
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:8501",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200

    assert response.headers.get(
        "access-control-allow-origin"
    ) == "http://localhost:8501"

def test_root_contains_environment():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "environment" in data
    assert data["environment"]

def test_ask_endpoint_handles_unexpected_error(
    monkeypatch,
):
    class ErrorService:
        def answer_response(self, question):
            raise RuntimeError(
                "Unexpected internal failure."
            )

    monkeypatch.setattr(
        routes,
        "_service",
        ErrorService(),
    )

    response = client.post(
        "/api/ask",
        json={
            "question": "What is our revenue?"
        },
    )

    assert response.status_code == 500

    error_payload = response.json()

    assert error_payload["error"]["code"] == (
        "DECISION_ANALYSIS_FAILED"
    )

    assert error_payload["error"]["message"] == (
        "Decision analysis failed."
    )

    assert error_payload["error"]["status"] == 500