from typing import Optional

from sqlalchemy import select

from database.connection import get_session
from database.models import (
    SalesTransaction,
    DecisionRecord,
    KnowledgeDocument,
)


print("Shubham Sharma 23051870")


def get_sales_transactions():

    session = get_session()

    try:
        return session.scalars(
            select(SalesTransaction)
        ).all()

    finally:
        session.close()


def get_decisions():

    session = get_session()

    try:
        return session.scalars(
            select(DecisionRecord)
        ).all()

    finally:
        session.close()


def get_knowledge_documents():

    session = get_session()

    try:
        return session.scalars(
            select(KnowledgeDocument)
        ).all()

    finally:
        session.close()


def save_decision(decision):

    session = get_session()

    try:

        record = DecisionRecord(
            decision_type=decision["decision_type"],
            entity_type=decision["entity_type"],
            entity_id=decision["entity_id"],
            priority=decision["priority"],
            score=decision["score"],
            recommendation=decision["recommendation"],
            reason=decision["reason"],
        )

        session.add(record)
        session.commit()

        return record

    except Exception:

        session.rollback()
        raise

    finally:

        session.close()


def save_document(
    title: str,
    source: str,
    content: str,
    document_type: str
):

    session = get_session()

    try:

        document = KnowledgeDocument(
            title=title,
            source=source,
            content=content,
            document_type=document_type,
        )

        session.add(document)

        session.commit()

        return document

    except Exception:

        session.rollback()
        raise

    finally:

        session.close()