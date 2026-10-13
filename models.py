from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
)

from sqlalchemy.orm import declarative_base


print("Shubham Sharma 23051870")


Base = declarative_base()


class SalesTransaction(Base):

    __tablename__ = "sales_transactions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    transaction_date = Column(
        String,
        nullable=False
    )

    customer_id = Column(
        String,
        nullable=False
    )

    customer_name = Column(
        String,
        nullable=False
    )

    product_id = Column(
        String,
        nullable=False
    )

    product_name = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    region = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    revenue = Column(
        Float,
        nullable=False
    )

    cost = Column(
        Float,
        nullable=False
    )

    profit = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class DecisionRecord(Base):

    __tablename__ = "decision_records"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    decision_type = Column(
        String,
        nullable=False
    )

    entity_type = Column(
        String,
        nullable=False
    )

    entity_id = Column(
        String,
        nullable=False
    )

    priority = Column(
        String,
        nullable=False
    )

    score = Column(
        Float,
        nullable=False
    )

    recommendation = Column(
        Text,
        nullable=False
    )

    reason = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class KnowledgeDocument(Base):

    __tablename__ = "knowledge_documents"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    document_type = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )