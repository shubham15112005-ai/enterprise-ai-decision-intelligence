from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.decision_service import DecisionService
from utils.logger import get_logger


print("Shubham Sharma 23051870")


logger = get_logger(__name__)
class DecisionAPIError(Exception):
    """
    Application-level API error.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status: int,
    ):
        self.code = code
        self.message = message
        self.status = status

        super().__init__(message)


router = APIRouter(
    prefix="/api",
    tags=["Decision Intelligence"],
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Natural-language business question.",
    )


_service: DecisionService | None = None


def get_service() -> DecisionService:
    """
    Lazily create the DecisionService.
    """
    global _service

    if _service is None:
        logger.info(
            "Initializing DecisionService"
        )

        _service = DecisionService()

    return _service


@router.get("/health")
def health() -> dict[str, Any]:
    """
    API health endpoint.
    """
    logger.info(
        "Health check requested"
    )

    service = get_service()

    result = service.health_check()

    logger.info(
        "Health check completed | status=%s",
        result.get("status"),
    )

    return result


@router.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Answer a natural-language business question.
    """
    logger.info(
        "Decision request received | question=%r",
        request.question,
    )

    try:
        service = get_service()

        response = service.answer_response(
            request.question
        )

        logger.info(
            "Decision request completed | "
            "route=%s | llm_used=%s | evidence=%s",
            response.route.route,
            response.llm_used,
            response.evidence_available,
        )

        return response.to_dict()

    except ValueError as exc:
        logger.warning(
            "Invalid decision request | error=%s",
            exc,
        )

        raise DecisionAPIError(
            code="INVALID_QUESTION",
            message=str(exc),
            status=400,
        ) from exc


    except TypeError as exc:
        logger.warning(
            "Invalid request type | error=%s",
            exc,
        )

        raise DecisionAPIError(
            code="INVALID_REQUEST",
            message=str(exc),
            status=400,
        ) from exc

    except Exception as exc:
        logger.exception(
            "Decision analysis failed | error=%s",
            exc,
        )

        raise DecisionAPIError(
            code="DECISION_ANALYSIS_FAILED",
            message="Decision analysis failed.",
            status=500,
        ) from exc