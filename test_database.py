from database.models import (
    Base,
    SalesTransaction,
    DecisionRecord,
    KnowledgeDocument,
)


print("Shubham Sharma 23051870")


def test_database_models_exist():

    assert SalesTransaction.__tablename__ == (
        "sales_transactions"
    )

    assert DecisionRecord.__tablename__ == (
        "decision_records"
    )

    assert KnowledgeDocument.__tablename__ == (
        "knowledge_documents"
    )


def test_database_tables():

    tables = Base.metadata.tables

    assert "sales_transactions" in tables
    assert "decision_records" in tables
    assert "knowledge_documents" in tables


def test_sales_columns():

    columns = (
        SalesTransaction
        .__table__
        .columns
    )

    assert "customer_id" in columns
    assert "product_id" in columns
    assert "revenue" in columns
    assert "profit" in columns


def test_decision_columns():

    columns = (
        DecisionRecord
        .__table__
        .columns
    )

    assert "decision_type" in columns
    assert "priority" in columns
    assert "score" in columns
    assert "recommendation" in columns