import pandas as pd
import pytest

from services.decision_service import DecisionService

print("Shubham Sharma 23051870")


class FakeOrchestrator:
    """Minimal fake orchestrator for service-layer testing."""

    def __init__(self):
        self.calls = []

    def analyze(self, question, df):
        self.calls.append(
            {
                "question": question,
                "rows": len(df),
            }
        )

        return {
            "question": question,
            "route": "TOTAL_REVENUE",
            "answer": "Revenue analysis completed.",
            "llm_used": False,
        }


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "customer_name": ["Customer A", "Customer B"],
            "product_id": ["P001", "P002"],
            "product_name": ["Product A", "Product B"],
            "category": ["Electronics", "Software"],
            "region": ["North", "South"],
            "quantity": [2, 3],
            "unit_price": [100.0, 200.0],
            "revenue": [200.0, 600.0],
            "cost": [100.0, 300.0],
            "profit": [100.0, 300.0],
        }
    )


def test_service_accepts_dataframe(sample_dataframe):
    orchestrator = FakeOrchestrator()

    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=orchestrator,
    )

    df = service.get_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_answer_calls_orchestrator(sample_dataframe):
    orchestrator = FakeOrchestrator()

    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=orchestrator,
    )

    result = service.answer("What is our total revenue?")

    assert result["route"] == "TOTAL_REVENUE"
    assert result["answer"] == "Revenue analysis completed."

    assert len(orchestrator.calls) == 1
    assert orchestrator.calls[0]["question"] == "What is our total revenue?"
    assert orchestrator.calls[0]["rows"] == 2


def test_answer_strips_question(sample_dataframe):
    orchestrator = FakeOrchestrator()

    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=orchestrator,
    )

    service.answer("   What is our revenue?   ")

    assert orchestrator.calls[0]["question"] == "What is our revenue?"


def test_empty_question_is_rejected(sample_dataframe):
    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=FakeOrchestrator(),
    )

    with pytest.raises(ValueError):
        service.answer("")


def test_whitespace_question_is_rejected(sample_dataframe):
    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=FakeOrchestrator(),
    )

    with pytest.raises(ValueError):
        service.answer("     ")


def test_non_string_question_is_rejected(sample_dataframe):
    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=FakeOrchestrator(),
    )

    with pytest.raises(TypeError):
        service.answer(123)


def test_refresh_data(sample_dataframe):
    initial_data = sample_dataframe.iloc[:1].copy()

    new_data = sample_dataframe.copy()
    new_data.loc[len(new_data)] = [
        "C003",
        "Customer C",
        "P003",
        "Product C",
        "Hardware",
        "East",
        5,
        50.0,
        250.0,
        125.0,
        125.0,
    ]

    service = DecisionService(
        dataframe=initial_data,
        orchestrator=FakeOrchestrator(),
    )

    assert len(service.get_dataframe()) == 1

    refreshed = service.refresh_data(new_data)

    assert len(refreshed) == 3
    assert len(service.get_dataframe()) == 3


def test_refresh_data_rejects_invalid_dataframe(sample_dataframe):
    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=FakeOrchestrator(),
    )

    with pytest.raises(TypeError):
        service.refresh_data("invalid")


def test_health_check(sample_dataframe):
    service = DecisionService(
        dataframe=sample_dataframe,
        orchestrator=FakeOrchestrator(),
    )

    health = service.health_check()

    assert health["service"] == "DecisionService"
    assert health["status"] == "healthy"
    assert health["data_available"] is True
    assert health["row_count"] == 2
    assert health["orchestrator_available"] is True